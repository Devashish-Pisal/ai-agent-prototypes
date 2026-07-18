from loguru import logger
from invoice_processor import InvoiceProcessor


def main():
    logger.info("Starting invoice processor")
    processor = InvoiceProcessor()
    processor.run()
    logger.info("Finished")


if __name__ == "__main__":
    main()