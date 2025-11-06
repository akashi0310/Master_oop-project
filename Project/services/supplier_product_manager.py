from typing import List
from domain.interfaces.supplier_interfaces import SupplierProductManagement


class SupplierProductManager(SupplierProductManagement):
    """Manages the products supplied by a supplier"""
    
    def __init__(self, initial_products: List[int] = None):
        self._products_supplied = initial_products or []
    
    def add_product(self, product_id: int) -> None:
        """Add a product ID to the list of products supplied"""
        if product_id <= 0:
            raise ValueError("Product ID must be positive")
        if product_id not in self._products_supplied:
            self._products_supplied.append(product_id)
    
    def remove_product(self, product_id: int) -> None:
        """Remove a product ID from the list of products supplied"""
        if product_id in self._products_supplied:
            self._products_supplied.remove(product_id)
    
    def get_product_count(self) -> int:
        """Get the number of products supplied by this supplier"""
        return len(self._products_supplied)
    
    def supplies_product(self, product_id: int) -> bool:
        """Check if the supplier supplies a specific product"""
        return product_id in self._products_supplied
    
    @property
    def products_supplied(self) -> List[int]:
        """Get the list of products supplied"""
        return self._products_supplied.copy()