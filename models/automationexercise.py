"""Records for the automationexercise.com site and its API."""
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


@dataclass
class PaymentDetails:
    name: str
    card_number: str
    cvc: str
    expiry_month: str
    expiry_year: str


@dataclass
class Product:
    """A product as the product-details page shows it."""

    name: str
    category: str
    price: str
    availability: str
    condition: str
    brand: str


@dataclass
class CartProduct:
    """A cart row. Compared whole against what a test expected, which is what
    the generated __eq__ is here for."""

    name: str
    category: str
    price: str
    quantity: int
    total: str

    @property
    def unit_price(self):
        return int(self.price.replace("Rs.", "").strip())

    @property
    def total_price(self):
        return int(self.total.replace("Rs.", "").strip())
