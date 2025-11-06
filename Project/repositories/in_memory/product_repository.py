from typing import List, Optional
from domain.models import Product
from repositories.interfaces.product_repository import ProductRepository


class InMemoryProductRepository(ProductRepository):
    """In-memory implementation of ProductRepository"""
    
    def __init__(self):
        self._products: List[Product] = []
    
    def add(self, product: Product) -> None:
        """Add a new product to the repository"""
        if any(p.product_id == product.product_id for p in self._products):
            raise ValueError(f"Product with ID {product.product_id} already exists")
        self._products.append(product)
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get a product by its ID"""
        for product in self._products:
            if product.product_id == product_id:
                return product
        return None
    
    def get_all(self) -> List[Product]:
        """Get all products in the repository"""
        return self._products.copy()
    
    def update(self, product: Product) -> bool:
        """Update an existing product"""
        for i, existing_product in enumerate(self._products):
            if existing_product.product_id == product.product_id:
                self._products[i] = product
                return True
        return False
    
    def delete(self, product_id: int) -> bool:
        """Delete a product by its ID"""
        for i, product in enumerate(self._products):
            if product.product_id == product_id:
                del self._products[i]
                return True
        return False
    
    def get_by_category(self, category: str) -> List[Product]:
        """Get all products in a specific category"""
        return [p for p in self._products if p.category.lower() == category.lower()]
    
    def get_by_supplier(self, supplier_id: int) -> List[Product]:
        """Get all products from a specific supplier"""
        return [p for p in self._products if p.supplier_id == supplier_id]
    
    def get_in_stock(self) -> List[Product]:
        """Get all products that are currently in stock"""
        return [p for p in self._products if p.is_in_stock()]
    
    def get_out_of_stock(self) -> List[Product]:
        """Get all products that are out of stock"""
        return [p for p in self._products if not p.is_in_stock()]
    
    def search(self, query: str) -> List[Product]:
        """Search for products by name or category"""
        query = query.lower()
        return [
            p for p in self._products 
            if query in p.name.lower() or query in p.category.lower()
        ]