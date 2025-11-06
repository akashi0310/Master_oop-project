from typing import Union
from ..value_objects.money import Money


class Product:
    def __init__(
        self,
        product_id: int,
        name: str,
        price: Union[float, Money],
        quantity_available: int,
        category: str,
        weight: float,
        supplier_id: int
    ):
        if not name or not name.strip():
            raise ValueError("Product name cannot be empty")
        if product_id <= 0:
            raise ValueError("Product ID must be positive")
        if quantity_available < 0:
            raise ValueError("Quantity available cannot be negative")
        if weight <= 0:
            raise ValueError("Weight must be positive")
        if supplier_id <= 0:
            raise ValueError("Supplier ID must be positive")
        if not category or not category.strip():
            raise ValueError("Category cannot be empty")
        
        self.product_id = product_id
        self.name = name.strip()
        self.price = Money(price) if isinstance(price, (float, int)) else price
        self.quantity_available = quantity_available
        self.category = category.strip()
        self.weight = weight
        self.supplier_id = supplier_id
        self.discount_eligible = True

    def is_in_stock(self) -> bool:
        """Check if product is in stock"""
        return self.quantity_available > 0
    
    def has_sufficient_stock(self, requested_quantity: int) -> bool:
        """Check if there's sufficient stock for the requested quantity"""
        if requested_quantity <= 0:
            raise ValueError("Requested quantity must be positive")
        return self.quantity_available >= requested_quantity
    
    def reduce_stock(self, quantity: int) -> None:
        """Reduce stock by the specified quantity"""
        if quantity <= 0:
            raise ValueError("Quantity to reduce must be positive")
        if not self.has_sufficient_stock(quantity):
            raise ValueError(f"Insufficient stock. Available: {self.quantity_available}, Requested: {quantity}")
        self.quantity_available -= quantity
    
    def increase_stock(self, quantity: int) -> None:
        """Increase stock by the specified quantity"""
        if quantity <= 0:
            raise ValueError("Quantity to increase must be positive")
        self.quantity_available += quantity
    
    def update_price(self, new_price: Union[float, Money]) -> None:
        """Update the product price"""
        self.price = Money(new_price) if isinstance(new_price, (float, int)) else new_price
    
    def is_low_stock(self, threshold: int = 10) -> bool:
        """Check if product is low in stock"""
        return self.quantity_available <= threshold
    
    def get_total_value(self) -> Money:
        """Get total value of current stock"""
        return self.price.multiply(self.quantity_available)
    
    def __repr__(self) -> str:
        return f"<Product {self.name} ({self.price})>"
