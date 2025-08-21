from pathlib import Path
import whisper
from .file import File
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class AudioTranscriber:
    def __init__(self, model_size: str):
        self.model_size = model_size
        # TODO Add cache dir - self.cache_dir = cache_dir
        self.model = whisper.load_model(model_size)
    
    def transcribe(self, file_obj: File) -> str:
        logger.info(f"Transcribing file: {file_obj.path.name}")
        result = self.model.transcribe(str(file_obj.path), fp16 = False)
        logger.info(f"Transcription complete for {file_obj.path.name}")
        file_obj.is_transcribed = True
        file_obj.contents = result["text"]
        return result["text"]
    
        # TODO Save metadata into file object
        
        
        
        