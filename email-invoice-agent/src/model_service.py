from pathlib import Path
import os
import time
import fitz
from pprint import pprint
from dotenv import load_dotenv
from google import genai
from google.genai import types
from loguru import logger
from schemas import InvoiceResult


load_dotenv()


class ModelService:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.prompt = Path("E:\\(_Coding_Data_)\\(_Github_Repositories_)\\ai-agent-prototypes\\email-invoice-agent\\prompts\\invoice_classifier.txt").read_text(encoding="utf-8")
        self.models = [
            "gemini-3-flash-preview",
            "gemini-2.5-flash",
            "gemini-3.1-flash-lite-preview",
            "gemini-2.5-flash-lite"
        ]
        self.max_retries = 3


    def classify_invoice(self, pdf_bytes: bytes) -> InvoiceResult:
        document = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in document:
            text += page.get_text()
        for model in self.models:
            for attempt in range(1, self.max_retries + 1):
                try:
                    logger.info(
                        "Trying model '{}' ({}/{})",
                        model,
                        attempt,
                        self.max_retries
                    )
                    response = self.client.models.generate_content(
                        model=model,
                        contents=f"{self.prompt}\n\n{text}",
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=InvoiceResult,
                            temperature=0
                        )
                    )
                    result: InvoiceResult = response.parsed
                    logger.success(
                        "Classification complete | model={} invoice={} vendor={}",
                        model,
                        result.is_invoice,
                        result.vendor
                    )
                    logger.info("Model output: {}", str(result))
                    return result
                except Exception as e:
                    logger.warning(
                        "Model '{}' failed ({}/{}): {}",
                        model,
                        attempt,
                        self.max_retries,
                        e
                    )
                    if attempt < self.max_retries:
                        time.sleep(2)
        raise RuntimeError("All Gemini models failed.")