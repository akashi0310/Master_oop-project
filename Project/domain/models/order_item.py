from typing import Union
from ..value_objects.money import Money


class OrderItem:
    def __init__(
        self,
        product_id: int,
        quantity: int,
        unit_price: Union[float, Money],
        weight: float = 0.0
    ):
        if product_id <= 0:
            raise ValueError("Product ID must be positive")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if isinstance(unit_price, (int, float)) and unit_price <= 0:
            raise ValueError("Unit price must be positive")
        if isinstance(unit_price, Money) and unit_price.amount <= 0:
            raise ValueError("Unit price must be positive")
        if weight < 0:
            raise ValueError("Weight cannot be negative")
        
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = Money(unit_price) if isinstance(unit_price, (float, int)) else unit_price
        self.weight = weight
        self.discount_applied = Money(0.0)
    
    def get_total_price(self) -> Money:
        """Calculate the total price for this order item"""
        return self.unit_price.multiply(self.quantity)
    
    def get_total_price_after_discount(self) -> Money:
        """Calculate the total price after applying discount"""
        return self.get_total_price().subtract(self.discount_applied)
    
    def apply_discount(self, discount_amount: Union[float, Money]) -> None:
        """Apply a discount to this order item"""
        discount = Money(discount_amount) if isinstance(discount_amount, (float, int)) else discount_amount
        if discount.is_greater_than(self.get_total_price()):
            raise ValueError("Discount cannot exceed total price")
        self.discount_applied = discount
    
    def apply_discount_percentage(self, discount_percent: float) -> None:
        """Apply a discount percentage to this order item"""
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount percent must be between 0 and 100")
        discount_amount = self.get_total_price().multiply(discount_percent / 100)
        self.apply_discount(discount_amount)
    
    def get_total_weight(self) -> float:
        """Calculate the total weight for this order item"""
        return self.weight * self.quantity
    
    def update_quantity(self, new_quantity: int) -> None:
        """Update the quantity of this order item"""
        if new_quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.quantity = new_quantity
    
    def update_unit_price(self, new_price: Union[float, Money]) -> None:
        """Update the unit price of this order item"""
        if isinstance(new_price, (int, float)) and new_price <= 0:
            raise ValueError("Unit price must be positive")
        if isinstance(new_price, Money) and new_price.amount <= 0:
            raise ValueError("Unit price must be positive")
        self.unit_price = Money(new_price) if isinstance(new_price, (float, int)) else new_price
