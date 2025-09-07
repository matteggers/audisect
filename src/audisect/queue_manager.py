# Should initiate queues and manage them. The pipeline will use this to get files to process.
from collections import deque
from pathlib import Path
from .file_handler import FileHandler
from .file import File
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class QueueManager:
    def __init__(self):
        self.to_transcribe = deque()
        self.to_analyze = deque()
        self.to_analyze_post = deque()
        self.to_perform_stats = deque()
        self.transcription_quantity = 0
        self.analysis_quantity = 0
        self.successful_transcriptions = 0
        self.successful_analyses = 0
        
    def enqueue_for_transcription(self, file: File) -> None:
        if not isinstance(file, File):
            logger.error(f"Expected File object, got {type(file).__name__}")
            raise TypeError(f"enqueue_for_transcription expected File, got {type(file).__name__}: {file}")
        self.to_transcribe.append(file)
        self.transcription_quantity += 1
        logger.info(f"Enqueued {file.path.name} for transcription.")
        
    def dequeue_for_transcription(self) -> File:
        if self.to_transcribe:
            file = self.to_transcribe.popleft()
            return file
        else:
            logger.info("No files to dequeue for transcription.")
            return None
        
    def enqueue_for_analysis(self, file: File) -> None:
        if not isinstance(file, File):
            logger.error(f"Expected File object, got {type(file).__name__}")
            raise TypeError(f"enqueue_for_analysis expected File, got {type(file).__name__}: {file}")
        self.to_analyze.append(file)
        self.analysis_quantity += 1
        logger.info(f"Enqueued {file.path.name} for analysis.")
        
    def dequeue_for_analysis(self) -> File:
        if self.to_analyze:
            file = self.to_analyze.popleft()
            return file
        else:
            logger.info("No files to dequeue for analysis.")
            return None
        
    def enqueue_for_post_analysis(self, file: File) -> None:
        if not isinstance(file, File):
            logger.error(f"Expected File object, got {type(file).__name__}")
            raise TypeError(f"enqueue_for_post_analysis expected File, got {type(file).__name__}: {file}")
        self.to_analyze_post.append(file)
        self.analysis_quantity += 1
        logger.info(f"Enqueued {file.path.name} for post analysis.")
        
    def dequeue_for_post_analysis(self) -> File:
        if self.to_analyze_post:
            file = self.to_analyze_post.popleft()
            return file
        else:
            logger.info("No files to dequeue for post analysis.")
            return None
        
    def enqueue_for_stats(self, file: File) -> None:
        if not isinstance(file, File):
            logger.error(f"Expected File object, got {type(file).__name__}")
            raise TypeError(f"enqueue_for_stats expected File, got {type(file).__name__}: {file}")
        self.to_perform_stats.append(file)
        logger.info(f"Enqueued {file.path.name} for stats computation.")
        
    def dequeue_for_stats(self) -> File:
        if self.to_perform_stats:
            file = self.to_perform_stats.popleft()
            return file
        else:
            logger.info("No files to dequeue for stats computation.")
            return None
        
    def mark_transcription_success(self) -> None:
        self.successful_transcriptions += 1
        logger.info(f"Marked transcription success. Total successful transcriptions: {self.successful_transcriptions}")
    
    def mark_analysis_success(self) -> None:
        self.successful_analyses += 1
        logger.info(f"Marked analysis success. Total successful analyses: {self.successful_analyses}")
        
    def get_transcription_queue_size(self) -> int:
        return len(self.to_transcribe)
    
    def get_analysis_queue_size(self) -> int:
        return len(self.to_analyze)
    
    def transcription_queue_is_empty(self) -> bool:
        return len(self.to_transcribe) == 0
    
    def analysis_queue_is_empty(self) -> bool:
        return len(self.to_analyze) == 0
    
    def post_analysis_queue_is_empty(self) -> bool:
        return len(self.to_analyze_post) == 0
    
    def clear_queues(self) -> None:
        self.to_transcribe.clear()
        self.to_analyze.clear()
        logger.info("Cleared both transcription and analysis queues.")

        
    def queue_summary(self) -> str:
        failed_transcriptions = self.transcription_quantity - self.successful_transcriptions
        failed_analyses = self.analysis_quantity - self.successful_analyses
        summary = (
            f"Total transcriptions attempted: {self.transcription_quantity}, \n"
            f"Successful: {self.successful_transcriptions}, "
            f"Failed: {failed_transcriptions}\n"
            f"Total analyses attempted: {self.analysis_quantity}, \n"
            f"Successful: {self.successful_analyses}, "
            f"Failed: {failed_analyses}"
        )
