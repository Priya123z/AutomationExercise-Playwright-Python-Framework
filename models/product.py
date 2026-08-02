from dataclasses import dataclass


@dataclass
class Product:
    name: str
    category: str
    price: str
    availability: str
    condition: str
    brand: str
