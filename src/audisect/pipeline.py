from .file_handler import FileHandler
from .file import File
from .audio_transcriber import AudioTranscriber
from .sentiment_analyzer import SentimentAnalyzer
from collections import deque
import logging
import pandas as pd
from .queue_manager import QueueManager
from .file_locator import FileLocator
from .stats_manager import StatsManager

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
        self.handler = FileHandler(input_directory=input_dir, output_directory=output_dir)
        self.locator = FileLocator(input_directory=input_dir, output_directory=output_dir, allowed_extensions=[".mp3", ".wav", ".flac"])
        self.audio_transcriber = AudioTranscriber(model_size)
        self.sentiment_analyzer = SentimentAnalyzer(model)
        self.stats_manager = StatsManager(output_dir=output_dir)

        self.queue_manager = QueueManager()
        self.files = []
        
    def enqueue_all(self) -> None:
        self.files.clear()
        files_to_translate = self.locator.locate_all_audio_files()
        for file in files_to_translate:
            file_obj = self.handler.create_object(file)
            self.handler.set_output_paths(file_obj)
            self.files.append(file_obj)

            if not self.handler.file_exists(file, ".txt"):
                self.queue_manager.enqueue_for_transcription(file_obj)
                logger.info(f"Enqueued {file} for transcription")
            else:
                logger.info(f"{file} already transcribed, skipping transcription")

            if not self.handler.file_exists(file, ".csv"):
                self.queue_manager.enqueue_for_analysis(file_obj)
                logger.info(f"Enqueued {file} for analysis")
            else:
                logger.info(f"{file} already analyzed, skipping analysis")
    
    def enqueue_post_analysis(self) -> None:
        for file_obj in self.files:
            self.queue_manager.enqueue_for_post_analysis(file_obj)
            logger.info(f"Enqueued {file_obj.path.name} for post-analysis")
 
    def post_analyze_all(self) -> None:
        while not self.queue_manager.post_analysis_queue_is_empty():
            file_obj = self.queue_manager.dequeue_for_post_analysis()
            df = pd.read_csv(self.handler.get_csv_path(file_obj))
            self.stats_manager.compute_and_store_stats(df, file_obj.path.stem)
            logger.info(f"Post-analyzing {file_obj.path.name}")

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
                "model_neg": m[0], "model_neu": m[1], "model_pos": m[2], "model_weighted_avg": m[3],
                "vader_neg": v["neg"], "vader_neu": v["neu"], "vader_pos": v["pos"],
                "vader_compound": v["compound"],
            })

        
        out_df = pd.DataFrame(rows)
        csv_path = self.handler.get_csv_path(file)
        out_df.to_csv(csv_path, index=False)
        logger.info(f"Successfully analyzed {file.path.name}, results saved to {csv_path.name}")
        
    def transcribe_all(self) -> None:
        while not self.queue_manager.transcription_queue_is_empty():
            file_obj = self.queue_manager.dequeue_for_transcription()

            self.handler.write_file(
                file = file_obj,
                text = self.audio_transcriber.transcribe(file_obj),
                suffix = ".txt"
            )
            self.queue_manager.mark_transcription_success() 

    def analyze_all(self) -> None:
        while not self.queue_manager.analysis_queue_is_empty():
            file_obj = self.queue_manager.dequeue_for_analysis()
            self.perform_analysis(file_obj)
            
        
    def run(self):
        logger.info("Pipeline starting...") 
        logger.info(f"Input directory: {self.handler.input_directory}, Output directory: {self.handler.output_directory}")
        logger.info(f"Transcription model size: {self.audio_transcriber.model_size}, Sentiment model: {self.sentiment_analyzer.sentiment_model}")
        self.enqueue_all()
        self.transcribe_all()
        self.analyze_all()
        self.enqueue_post_analysis()
        self.post_analyze_all()
        logger.info("Pipeline finished")