from typing import List, Optional
from domain.models.product import Product
from domain.value_objects.money import Money


class InventoryManager:
    """Manages inventory operations for products"""
    
    def __init__(self):
        self._products: List[Product] = []
    
    def add_product(self, product: Product) -> None:
        """Add a product to inventory"""
        if any(p.product_id == product.product_id for p in self._products):
            raise ValueError(f"Product with ID {product.product_id} already exists")
        self._products.append(product)
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """Get a product by ID"""
        for product in self._products:
            if product.product_id == product_id:
                return product
        return None
    
    def get_all_products(self) -> List[Product]:
        """Get all products"""
        return self._products.copy()
    
    def check_stock(self, product_id: int, quantity: int) -> bool:
        """Check if product has sufficient stock"""
        product = self.get_product(product_id)
        if product:
            return product.has_sufficient_stock(quantity)
        return False
    
    def reduce_stock(self, product_id: int, quantity: int) -> None:
        """Reduce stock for a product"""
        product = self.get_product(product_id)
        if product:
            product.reduce_stock(quantity)
    
    def increase_stock(self, product_id: int, quantity: int) -> None:
        """Increase stock for a product"""
        product = self.get_product(product_id)
        if product:
            product.increase_stock(quantity)
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """Get products with low stock"""
        return [p for p in self._products if p.is_low_stock(threshold)]
    
    def get_total_inventory_value(self) -> Money:
        """Calculate total value of all inventory"""
        total = Money(0.0)
        for product in self._products:
            total = total.add(product.get_total_value())
        return total