"""
Ocean Professional Style - Models
Defines the Product domain model (data structure).
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    """
    Product domain model representing a product in the catalog.

    Fields:
        id: Unique identifier for the product.
        name: Human-readable product name.
        price: Unit price as a float (should be >= 0).
        quantity: Available stock quantity as an integer (should be >= 0).
    """
    id: int
    name: str
    price: float
    quantity: int

    @staticmethod
    def from_dict(data: dict, id_override: Optional[int] = None) -> "Product":
        """
        Create a Product instance from a dictionary.

        Args:
            data: A dict containing keys name, price, and quantity. id is optional if id_override is provided.
            id_override: If provided, overrides any id value in data.

        Returns:
            Product instance.
        """
        pid = data.get("id")
        if id_override is not None:
            pid = id_override
        return Product(
            id=int(pid) if pid is not None else 0,
            name=str(data["name"]),
            price=float(data["price"]),
            quantity=int(data["quantity"]),
        )
