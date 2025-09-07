from pathlib import Path

class FileLocator:
    def __init__(self, input_directory: Path, output_directory: Path, allowed_extensions: dict):
        self.input_directory = Path(input_directory)
        self.output_directory = Path(output_directory)
        self.extensions = allowed_extensions or {".wav", ".mp3", ".m4a", ".mp4"}
        
    def locate_all_audio_files(self) -> list[Path]:
        files = []
        for file in self.input_directory.glob("*"):
            if file.suffix.lower() in self.extensions:
                files.append(file)
        return files
    
    def locate_all_csv_files(self) -> list[Path]:
        csv_dir = self.output_directory / "csv"
        if not csv_dir.exists():
            return []
        return list(csv_dir.glob("*.csv"))