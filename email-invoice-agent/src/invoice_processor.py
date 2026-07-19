from loguru import logger
from email_service import EmailService
from model_service import ModelService
from storage_service import StorageService


class InvoiceProcessor:
    def __init__(self):
        self.email_service = EmailService()
        self.model_service = ModelService()
        self.storage_service = StorageService()

    def run(self):
        self.email_service.connect()
        try:
            attachments = self.email_service.fetch_unread_pdf_attachments()
            if not attachments:
                logger.info("No PDF attachments found")
                return
            for attachment in attachments:
                logger.info("="*100)
                logger.info("Processing attachment {}", attachment.filename)
                result = self.model_service.classify_invoice(attachment.data)
                if not result.is_invoice:
                    logger.info("{} is not an invoice", attachment.filename)
                    continue
                vendor = self._sanitize(result.vendor or "Unknown")
                invoice_number = self._sanitize(result.invoice_number or "Unknown")
                filename = f"{vendor}_{invoice_number}.pdf"
                self.storage_service.save_pdf(
                    filename=filename,
                    data=attachment.data
                )
            logger.info("=" * 100)
        except Exception as e:
            logger.error(e)



    @staticmethod
    def _sanitize(value: str) -> str:
        invalid = '<>:"/\\|?*'
        for char in invalid:
            value = value.replace(char, "_")
        return value.strip()