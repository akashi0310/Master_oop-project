from typing import Union, Optional
from ..value_objects.money import Money
from ..interfaces.product_interfaces import ProductInfo, StockOperations, PricingOperations
from services.product_validator import ProductValidator, DefaultProductValidator


class Product(
    ProductInfo,
    StockOperations,
    PricingOperations
):
    """
    Product entity that follows SOLID principles by delegating
    responsibilities to appropriate components.
    """
    
    def __init__(
        self,
        product_id: int,
        name: str,
        price: Union[float, Money],
        quantity_available: int,
        category: str,
        weight: float,
        supplier_id: int,
        validator: Optional[ProductValidator] = None
    ):
        # Use dependency injection for validation
        self._validator = validator or DefaultProductValidator()
        
        # Validate product data
        self._validator.validate_product_data(
            product_id, name, quantity_available, weight, supplier_id, category
        )
        
        # Set product attributes
        self.product_id = product_id
        self.name = name.strip()
        self.price = Money(price) if isinstance(price, (float, int)) else price
        self.quantity_available = quantity_available
        self.category = category.strip()
        self.weight = weight
        self.supplier_id = supplier_id
        self._discount_eligible = True
    
    # Properties for read-only access
    @property
    def discount_eligible(self) -> bool:
        """Check if product is eligible for discounts"""
        return self._discount_eligible
    
    # Stock operations
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
    
    def is_low_stock(self, threshold: int = 10) -> bool:
        """Check if product is low in stock"""
        return self.quantity_available <= threshold
    
    def get_total_value(self) -> Money:
        """Get the total value of current stock"""
        return self.price.multiply(self.quantity_available)
    
    # Pricing operations
    def update_price(self, new_price: Union[float, Money]) -> None:
        """Update the product price"""
        self.price = Money(new_price) if isinstance(new_price, (float, int)) else new_price
    
    def set_discount_eligibility(self, eligible: bool) -> None:
        """Set whether the product is eligible for discounts"""
        self._discount_eligible = eligible
    
    def __repr__(self) -> str:
        return f"<Product {self.name} ({self.price})>"
