from .file_handler import FileHandler
from .file import File
from .dataframe_store import DataframeStore
from .audio_transcriber import AudioTranscriber
from .sentiment_analyzer import SentimentAnalyzer
from collections import deque
import logging
import pandas as pd


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
    
class Pipeline:
    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        model_size: str = "base",
        model: str = "cardiffnlp/twitter-roberta-base-sentiment",
        model_alias: str = "",
    ):
        self.handler = FileHandler(input_directory=input_dir, output_directory=output_dir, allowed_extensions=[".mp3", ".wav", ".flac"])
        self.audio_transcriber = AudioTranscriber(model_size)
        self.dataframe_store = DataframeStore(model, model_alias)
        self.sentiment_analyzer = SentimentAnalyzer(model, self.dataframe_store) # This is custom, not SentimentIntensityAnalyzer from vader. FIXME make this more clear

        self.to_transcribe = deque()
        self.to_analyze = deque()

    def enqueue_transcription(self) -> None:
        files_to_translate = self.handler.locate_all_audio_files()
        for file in files_to_translate: # passing PATH but below is checking if file OBJECT
            if (not self.handler.file_exists(file, ".txt")):
                file_obj = self.handler.create_object(file)
                self.handler.set_output_paths(file_obj)
                self.to_transcribe.append(file_obj)
                self.to_analyze.append(file_obj)
                logger.info(f"Enqueued {file}")
            else:
                print(f"{file} already translated") # FIXME robust handling
    
    def transcribe_all(self) -> None:
        while (self.to_transcribe):
            file_obj = self.to_transcribe[0]
            self.handler.write_file(
                file=file_obj, 
                text=self.audio_transcriber.transcribe(file_obj), 
                suffix=".txt"
                )
            self.to_transcribe.popleft()
            # TODO Error handling
            
            
    # FIXME This is a bit messy, should be refactored AND passing the audio file instead of the txt right now. Update the attributes of file to have path to both
    
    def perform_analysis(self, file: File) -> None:
        
        if self.handler.file_exists(file.path, ".csv"):
            return

        contents = self.handler.read_file(file)
        sentences = self.sentiment_analyzer.tokenize_to_sentences(contents)

        rows = []
        for s in sentences:
            m = self.sentiment_analyzer.model_sentiment_scores(s)
            v = self.sentiment_analyzer.vader_sentiment_scores(s)
            rows.append({
                "sentence": s,
                "model_neg": m[0], "model_neu": m[1], "model_pos": m[2],
                "vader_neg": v["neg"], "vader_neu": v["neu"], "vader_pos": v["pos"],
                "vader_compound": v["compound"],
            })

        
        out_df = pd.DataFrame(rows)
        csv_path = self.handler.get_csv_path(file)
        out_df.to_csv(csv_path, index=False)
        logger.info(f"Successfully analyzed {file.path.name}, results saved to {csv_path.name}")
        
    def analyze_all(self) -> None:
        while self.to_analyze:
            file_obj = self.to_analyze.popleft()
            self.perform_analysis(file_obj)
        
    def run(self):
        logger.info("Pipeline starting...") 
        logger.info(f"Input directory: {self.handler.input_directory}, Output directory: {self.handler.output_directory}")
        logger.info(f"Transcription model size: {self.audio_transcriber.model_size}, Sentiment model: {self.sentiment_analyzer.sentiment_model}")
        self.enqueue_transcription()
        self.transcribe_all()
        self.analyze_all()
        logger.info("Pipeline finished")
        
    
    #@BUGFIX File is saving ONLY the first analysis to all the CSVs, need to reset the dataframe for each file
        
        
            
    