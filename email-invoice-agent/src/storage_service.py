from pathlib import Path
import os
from dotenv import load_dotenv
from config import *
from loguru import logger


load_dotenv()


class StorageService:
    def __init__(self):
        self.storage_path = STORAGE_DIR
        self.storage_path.mkdir(parents=True, exist_ok=True)


    def save_pdf(self, filename: str, data: bytes) -> Path:
        file_path = self.storage_path / filename
        with open(file_path, "wb") as file:
            file.write(data)
        logger.info("Saved invoice to '{}'", file_path.relative_to(Path(__file__).parent.parent))
        return file_path