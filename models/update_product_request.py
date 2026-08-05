from dataclasses import dataclass


@dataclass(slots=True)
class UpdateProductRequest:
    title: str
    price: float
    category: str