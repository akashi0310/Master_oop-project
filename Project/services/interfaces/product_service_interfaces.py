from typing import List, Optional
from domain.models import Product, Supplier
from domain.value_objects import Money


class ProductRepository:
    """Interface for product repository operations"""
    def add_product(self, product: Product) -> None:
        """Add a new product to the repository"""
        pass
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """Get a product by ID"""
        pass
    
    def get_all_products(self) -> List[Product]:
        """Get all products"""
        pass
    
    def update_product(self, product: Product) -> bool:
        """Update a product in the repository"""
        pass
    
    def remove_product(self, product_id: int) -> bool:
        """Remove a product from the repository"""
        pass


class ProductSearch:
    """Interface for product search operations"""
    def search_products(self, query: str) -> List[Product]:
        """Search products by name or category"""
        pass
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        pass
    
    def get_products_by_supplier(self, supplier_id: int) -> List[Product]:
        """Get products by supplier"""
        pass


class ProductInventoryManager:
    """Interface for product inventory operations"""
    def check_product_availability(self, product_id: int, quantity: int) -> bool:
        """Check if a product is available in requested quantity"""
        pass
    
    def get_products_in_stock(self) -> List[Product]:
        """Get all products that are in stock"""
        pass
    
    def get_out_of_stock_products(self) -> List[Product]:
        """Get all products that are out of stock"""
        pass
    
    def get_total_inventory_value(self) -> Money:
        """Calculate total value of all inventory"""
        pass