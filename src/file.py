from pathlib import Path

class File:
    def __init__(self, path: Path):
        self.path: Path = Path(path)
        self.txt_path: Path = None
        self.csv_path: Path = None
        self.contents: str = ""
        self.is_transcribed = False
        self.is_analyze = False

  