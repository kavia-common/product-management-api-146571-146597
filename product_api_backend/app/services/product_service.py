"""
Ocean Professional Style - Services
Service layer that abstracts persistence operations for Product entities.

Note:
- Uses in-memory storage for simplicity.
- Designed to be easily replaced with a real database (e.g., SQLAlchemy, Supabase).
"""

from typing import Dict, List, Optional
from threading import RLock

from app.models.product import Product


class NotFoundError(Exception):
    """Raised when a requested product is not found."""
    pass


class ConflictError(Exception):
    """Raised on conflicts such as duplicate IDs."""
    pass


class ProductService:
    """
    Service class for managing Product entities.
    Thread-safe operations through a re-entrant lock for in-memory store.
    """

    def __init__(self) -> None:
        self._store: Dict[int, Product] = {}
        self._next_id: int = 1
        self._lock = RLock()

    # PUBLIC_INTERFACE
    def list_products(self) -> List[Product]:
        """Return a list of all products."""
        with self._lock:
            return list(self._store.values())

    # PUBLIC_INTERFACE
    def get_product(self, product_id: int) -> Product:
        """Return a single product by id, or raise NotFoundError."""
        with self._lock:
            product = self._store.get(product_id)
            if product is None:
                raise NotFoundError(f"Product {product_id} not found")
            return product

    # PUBLIC_INTERFACE
    def create_product(self, name: str, price: float, quantity: int) -> Product:
        """Create and store a new product, returning the created instance."""
        with self._lock:
            pid = self._next_id
            self._next_id += 1
            product = Product(id=pid, name=name, price=price, quantity=quantity)
            self._store[pid] = product
            return product

    # PUBLIC_INTERFACE
    def update_product(
        self,
        product_id: int,
        name: Optional[str] = None,
        price: Optional[float] = None,
        quantity: Optional[int] = None,
    ) -> Product:
        """Update an existing product fields and return the updated instance."""
        with self._lock:
            product = self._store.get(product_id)
            if product is None:
                raise NotFoundError(f"Product {product_id} not found")
            if name is not None:
                product.name = name
            if price is not None:
                product.price = price
            if quantity is not None:
                product.quantity = quantity
            self._store[product_id] = product
            return product

    # PUBLIC_INTERFACE
    def delete_product(self, product_id: int) -> None:
        """Delete a product by id, or raise NotFoundError if not found."""
        with self._lock:
            if product_id not in self._store:
                raise NotFoundError(f"Product {product_id} not found")
            del self._store[product_id]


# Singleton instance for app-wide use (simple DI)
product_service = ProductService()
