from pydantic import BaseModel


class InvoiceResult(BaseModel):
    is_invoice: bool
    vendor: str | None = None
    invoice_number: str | None = None
    invoice_date: str | None = None
    total_amount: float | None = None
    currency: str | None = None