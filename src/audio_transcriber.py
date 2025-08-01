from pathlib import Path
import whisper
from .file import File
class AudioTranscriber:
    def __init__(self, model_size: str):
        self.model_size = model_size
        # TODO Add cache dir - self.cache_dir = cache_dir
        self.model = whisper.load_model(model_size)
    
    def transcribe(self, file_obj: File) -> str:
        result = self.model.transcribe(str(file_obj.path), fp16 = False)
        return result["text"]
    
        # TODO Save metadata into file object
        
        
        
        