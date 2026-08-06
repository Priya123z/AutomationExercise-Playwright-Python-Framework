from faker import Faker
from datetime import datetime
from models.AutomationExercise_UI_API_Models.user import User


class UserFactory:

    _fake = Faker()
    @classmethod
    def create(cls) -> User:
        return User(
            title=cls._fake.random_element(elements = ["Mr","Mrs"]),
            email= f"{cls._fake.user_name()}_{datetime.now():%Y%m%d%H%M%S}@example.com",
            password=cls._fake.password(),
            date_of_birth=str(cls._fake.random_int(1, 28)),
            months_of_birth=str(cls._fake.random_int(1, 12)),
            years_of_birth= str(cls._fake.random_int(1970,2021)),
            newsletter=cls._fake.boolean(),
            special_offers=cls._fake.boolean(),
            first_name=cls._fake.first_name(),
            last_name=cls._fake.last_name(),
            company=cls._fake.company(),
            address_one=cls._fake.street_address(),
            address_two=cls._fake.secondary_address(),
            country=cls._fake.random_element(elements = ["India","United States","Canada","Australia","Israel","New Zealand","Singapore"]),
            state=cls._fake.state(),
            city=cls._fake.city(),
            zipcode=cls._fake.postcode(),
            mobile_number=cls._fake.phone_number()
        )