from dataclasses import dataclass

@dataclass
class PaymentDetails:
    name: str
    card_number: str
    cvc: str
    expiry_month: str
    expiry_year: str