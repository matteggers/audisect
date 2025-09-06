from pathlib import Path
from typing import Optional

class File:
    def __init__(self, path: Path):
        self.path: Path = Path(path)
        self.txt_path: Optional[Path] = None
        self.csv_path: Optional[Path] = None
        self.contents: str = ""
        self.is_transcribed = False
        self.is_analyze = False

  