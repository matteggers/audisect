from .file_handler import FileHandler
from .file import File
from .dataframe_store import DataframeStore
from .audio_transcriber import AudioTranscriber
from .sentiment_analyzer import SentimentAnalyzer
from collections import deque
import logging


# @FUTURE
# Use threading to analyze more at once
# NEED NVIDIA DEV CONTAINER

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
        logger.info(f"Performing analysis on {file.path.name}, file is of type {type(file)}")
        if self.handler.file_exists(file.path, ".csv"):
            logger.info(f"CSV file already exists for {file.path.name}, skipping analysis.")
            return
        logger.info(f"Analyzing {file.path.name}...")
        
        
        contents = self.handler.read_file(file)
        sentences = self.sentiment_analyzer.tokenize_to_sentences(contents)
        #logger.info(f"Number of sentences in {file.path.name}: {len(sentences)}")
        
        for sentence in sentences:
            model_scores = self.sentiment_analyzer.model_sentiment_scores(sentence)
            vader_scores = self.sentiment_analyzer.vader_analyzer(sentence)
            self.dataframe_store.add_sentiment(model_scores, vader_scores, sentence)
        
        logger.info(f"Analysis complete for {file.path.name}, saving results.")
        csv_path = self.handler.get_csv_path(file)
        self.dataframe_store.df.to_csv(csv_path, index=True)
        logger.info(f"Analysis for {file.path.name} completed and saved to CSV.")
        #print(f"Reading from txt path: {txt_path}")
        #contents = self.handler.read_file(self.handler.get_txt_path(file))
        #sentences = self.sentiment_analyzer.tokenize_to_sentences(contents)
        #logger.info(f"Number of sentences in {file.path.name}: {len(sentences)}")   

        #for sentence in sentences:
        #    model_scores = self.sentiment_analyzer.model_sentiment_scores(sentence)
        #    vader_scores = self.sentiment_analyzer.vader_analyzer(sentence)
        #    self.dataframe_store.add_sentiment(self.dataframe_store, model_scores, vader_scores)

        # FIXME Path injection vulnerability
        #csv_path = self.handler.get_csv_path(file)
        #self.dataframe_store.df.to_csv(csv_path, index=True)
        
        
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
        
    
    @BUGFIX File is saving ONLY the first analysis to all the CSVs, need to reset the dataframe for each file
        
        
            
    