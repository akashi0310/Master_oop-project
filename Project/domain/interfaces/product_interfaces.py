from typing import Protocol
from domain.value_objects.money import Money


class ProductInfo(Protocol):
    """Protocol for basic product information"""
    product_id: int
    name: str
    price: Money
    quantity_available: int
    category: str
    weight: float
    supplier_id: int


class StockOperations(Protocol):
    """Protocol for stock management operations"""
    def is_in_stock(self) -> bool:
        ...
    
    def has_sufficient_stock(self, requested_quantity: int) -> bool:
        ...
    
    def reduce_stock(self, quantity: int) -> None:
        ...
    
    def increase_stock(self, quantity: int) -> None:
        ...
    
    def is_low_stock(self, threshold: int = 10) -> bool:
        ...
    
    def get_total_value(self) -> Money:
        ...


class PricingOperations(Protocol):
    """Protocol for pricing operations"""
    def update_price(self, new_price: Money) -> None:
        ...
    
    def set_discount_eligibility(self, eligible: bool) -> None:
        ...