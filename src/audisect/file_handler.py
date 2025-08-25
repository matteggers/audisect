from pathlib import Path
from glob import glob
from .file import File
import logging

# Handles the creation of file objects

# Note:
# File Handler performs the following:
# Initializes itself and locates all audio files in the input directory
# 
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class FileHandler:
    def __init__(self, input_directory: Path, output_directory: Path, allowed_extensions: dict) -> Path:
        self.input_directory = Path(input_directory)
        self.output_directory = Path(output_directory)
        self.extensions = allowed_extensions or {".wav", ".mp3", ".m4a", ".mp4"}
        
        self.output_directory.mkdir(parents = True, exist_ok=True)
        
        self.csv_directory = self.output_directory / "csv"
        self.csv_directory.mkdir(parents = True, exist_ok=True)
        
        self.txt_directory = self.output_directory / "txt"
        self.txt_directory.mkdir(parents = True, exist_ok=True)
        
    def locate_all_audio_files(self) -> list[Path]:
        files = []
        for file in self.input_directory.glob("*"):
            if file.suffix.lower() in self.extensions:
                files.append(file)
                logger.info(f"Located audio file: {file.name}")
        return files
    
    def create_object(self, file: Path) -> File:
        return File(file)
    
    # Could just put this in creator
    def set_output_paths(self, file: File) -> None:
        file_name = file.path.stem
        file.txt_path = self.txt_directory / f"{file_name}.txt"
        file.csv_path = self.csv_directory / f"{file_name}.csv"

    def get_txt_path(self, file_obj: File) -> Path:
        if not isinstance(file_obj, File):
            logger.error(f"Expected File object, got {type(file_obj).__name__}")
            raise TypeError(f"get_txt_path expected File, got {type(file_obj).__name__}: {file_obj}")
        if file_obj.txt_path is None:
            self.set_output_paths(file_obj)
        return file_obj.txt_path
    
    def get_csv_path(self, file_obj: File) -> Path:
        return file_obj.csv_path
    
    def file_exists(self, file_path: Path, suffix: str) -> bool:
        file_name = file_path.stem
        if suffix == ".txt":
            return (self.txt_directory / f"{file_name}.txt").exists()
        elif suffix == ".csv":
            
            return (self.csv_directory / f"{file_name}.csv").exists()
        return False


    def read_file(self, file: File) -> str:
        txt_path = self.get_txt_path(file)
        try:
            return txt_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return txt_path.read_text(encoding="latin-1")
    

    def write_file(self, file: File, text: str, suffix: str) -> None:
        if (suffix == ".txt"):
            destination_path = self.get_txt_path(file)
        elif (suffix == ".csv"):
            destination_path = self.get_csv_path(file)
            
        destination_path.write_text(text, encoding="utf-8")        
    