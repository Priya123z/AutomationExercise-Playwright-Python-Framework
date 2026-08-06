from faker import Faker

from models.AutomationExercise_UI_API_Models.payment_detail import PaymentDetails


class PaymentFactory:
    _fake = Faker()

    @classmethod
    def valid(cls) -> PaymentDetails:
        return PaymentDetails(
            name=cls._fake.name(),
            card_number=cls._fake.credit_card_number(),
            cvc=cls._fake.credit_card_security_code(),
            expiry_month=str(cls._fake.month()),
            expiry_year=str(cls._fake.year()),

        )
