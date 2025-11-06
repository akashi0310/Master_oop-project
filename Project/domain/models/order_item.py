from typing import Union, Protocol
from ..value_objects.money import Money


class PricingCalculator(Protocol):
    """Protocol for calculating pricing"""
    def calculate_total(self, unit_price: Money, quantity: int) -> Money:
        ...


class DiscountCalculator(Protocol):
    """Protocol for calculating discounts"""
    def calculate_discount(self, total_price: Money) -> Money:
        ...


class OrderItem:
    """
    Order item entity that follows SOLID principles.
    Delegates calculations to specialized components.
    """
    
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
        self._discount_applied = Money(0.0)
    
    @property
    def discount_applied(self) -> Money:
        """Get the discount applied to this order item"""
        return self._discount_applied
    
    def get_total_price(self, pricing_calculator: PricingCalculator = None) -> Money:
        """Calculate the total price for this order item"""
        calculator = pricing_calculator or DefaultPricingCalculator()
        return calculator.calculate_total(self.unit_price, self.quantity)
    
    def get_total_price_after_discount(
        self,
        pricing_calculator: PricingCalculator = None,
        discount_calculator: DiscountCalculator = None
    ) -> Money:
        """Calculate the total price after applying discount"""
        total_price = self.get_total_price(pricing_calculator)
        calculator = discount_calculator or NoDiscountCalculator()
        # Use the already applied discount if no calculator provided
        if discount_calculator is None:
            discount = self._discount_applied
        else:
            discount = calculator.calculate_discount(total_price)
        return total_price.subtract(discount)
    
    def apply_discount(self, discount_amount: Union[float, Money]) -> None:
        """Apply a discount to this order item"""
        discount = Money(discount_amount) if isinstance(discount_amount, (float, int)) else discount_amount
        total_price = self.get_total_price()
        if discount.is_greater_than(total_price):
            raise ValueError("Discount cannot exceed total price")
        self._discount_applied = discount
    
    def apply_discount_percentage(self, discount_percent: float) -> None:
        """Apply a discount percentage to this order item"""
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount percent must be between 0 and 100")
        total_price = self.get_total_price()
        discount_amount = total_price.multiply(discount_percent / 100)
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


class DefaultPricingCalculator:
    """Default implementation of pricing calculator"""
    
    def calculate_total(self, unit_price: Money, quantity: int) -> Money:
        """Calculate total price by multiplying unit price by quantity"""
        return unit_price.multiply(quantity)


class NoDiscountCalculator:
    """Implementation that applies no discount"""
    
    def calculate_discount(self, total_price: Money) -> Money:
        """Return zero discount"""
        return Money(0.0)


class PercentageDiscountCalculator:
    """Implementation that applies percentage-based discounts"""
    
    def __init__(self, percentage: float):
        if percentage < 0 or percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        self.percentage = percentage
    
    def calculate_discount(self, total_price: Money) -> Money:
        """Calculate discount as a percentage of total price"""
        return total_price.multiply(self.percentage / 100)
