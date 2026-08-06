from dataclasses import dataclass


@dataclass(frozen=True)
class CartProduct:
    name: str
    category: str
    price: str
    quantity: int
    total: str

    @property
    def unit_price(self) -> int:
        return int(self.price.replace("Rs.", "").strip())

    @property
    def total_price(self) -> int:
        return int(self.total.replace("Rs.", "").strip())
