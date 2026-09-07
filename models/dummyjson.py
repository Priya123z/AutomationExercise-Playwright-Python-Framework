"""Request bodies for the dummyjson.com API."""
from dataclasses import dataclass


@dataclass
class LoginRequest:
    username: str
    password: str


@dataclass
class CreateProductRequest:
    title: str
    description: str
    category: str
    price: float


@dataclass
class UpdateProductRequest:
    title: str
    price: float
    category: str
