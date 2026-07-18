from pathlib import Path
import os
from dotenv import load_dotenv
from loguru import logger


load_dotenv()


class StorageService:
    def __init__(self):
        self.storage_path = Path("E:\\(_Coding_Data_)\\(_Github_Repositories_)\\ai-agent-prototypes\\email-invoice-agent\\storage")
        self.storage_path.mkdir(parents=True, exist_ok=True)


    def save_pdf(self, filename: str, data: bytes) -> Path:
        file_path = self.storage_path / filename
        with open(file_path, "wb") as file:
            file.write(data)
        logger.info("Saved invoice to {}", file_path)
        return file_path