from typing import List, Optional
from domain.models import Product


class ProductRepository:
    """Repository interface for Product entities"""
    
    def add(self, product: Product) -> None:
        """Add a new product to the repository"""
        raise NotImplementedError
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get a product by its ID"""
        raise NotImplementedError
    
    def get_all(self) -> List[Product]:
        """Get all products in the repository"""
        raise NotImplementedError
    
    def update(self, product: Product) -> bool:
        """Update an existing product"""
        raise NotImplementedError
    
    def delete(self, product_id: int) -> bool:
        """Delete a product by its ID"""
        raise NotImplementedError
    
    def get_by_category(self, category: str) -> List[Product]:
        """Get all products in a specific category"""
        raise NotImplementedError
    
    def get_by_supplier(self, supplier_id: int) -> List[Product]:
        """Get all products from a specific supplier"""
        raise NotImplementedError
    
    def get_in_stock(self) -> List[Product]:
        """Get all products that are currently in stock"""
        raise NotImplementedError
    
    def get_out_of_stock(self) -> List[Product]:
        """Get all products that are out of stock"""
        raise NotImplementedError
    
    def search(self, query: str) -> List[Product]:
        """Search for products by name or category"""
        raise NotImplementedError