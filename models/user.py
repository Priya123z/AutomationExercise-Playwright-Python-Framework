from dataclasses import dataclass


@dataclass
class User:

    title: str

    email: str
    password: str

    date_of_birth: str
    months_of_birth: str
    years_of_birth: str

    newsletter: bool
    special_offers: bool

    first_name: str
    last_name: str
    company: str

    address_one: str
    address_two: str

    country: str

    state: str
    city: str
    zipcode: str

    mobile_number: str
