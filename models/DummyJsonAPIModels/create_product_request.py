from dataclasses import dataclass


@dataclass(slots=True)
class CreateProductRequest:
    title: str
    description: str
    category: str
    price: float