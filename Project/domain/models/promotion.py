from typing import Union
from datetime import datetime
from ..value_objects.money import Money


class Promotion:
    def __init__(
        self,
        promo_id: int,
        code: str,
        discount_percent: float,
        min_purchase: Union[float, Money],
        valid_until: datetime,
        category: str = "all"
    ):
        if promo_id <= 0:
            raise ValueError("Promo ID must be positive")
        if not code or not code.strip():
            raise ValueError("Promo code cannot be empty")
        if discount_percent <= 0 or discount_percent > 100:
            raise ValueError("Discount percent must be between 0 and 100")
        if isinstance(min_purchase, (int, float)) and min_purchase < 0:
            raise ValueError("Minimum purchase cannot be negative")
        if isinstance(min_purchase, Money) and min_purchase.amount < 0:
            raise ValueError("Minimum purchase cannot be negative")
        if not isinstance(valid_until, datetime):
            raise ValueError("Valid until must be a datetime object")
        if not category or not category.strip():
            raise ValueError("Category cannot be empty")
        
        self.promo_id = promo_id
        self.code = code.strip().upper()
        self.discount_percent = discount_percent
        self.min_purchase = Money(min_purchase) if isinstance(min_purchase, (float, int)) else min_purchase
        self.valid_until = valid_until
        self.category = category.strip().lower()
        self.used_count = 0
        self.max_uses = None  # None means unlimited uses
    
    def is_valid(self) -> bool:
        """Check if the promotion is still valid"""
        return datetime.now() < self.valid_until
    
    def is_expired(self) -> bool:
        """Check if the promotion has expired"""
        return not self.is_valid()
    
    def is_applicable_to_category(self, product_category: str) -> bool:
        """Check if the promotion applies to a specific product category"""
        return self.category == "all" or self.category == product_category.lower()
    
    def meets_minimum_purchase(self, purchase_amount: Union[float, Money]) -> bool:
        """Check if the purchase amount meets the minimum requirement"""
        amount = Money(purchase_amount) if isinstance(purchase_amount, (float, int)) else purchase_amount
        return amount.is_greater_than(self.min_purchase) or amount.amount == self.min_purchase.amount
    
    def can_be_used(self) -> bool:
        """Check if the promotion can still be used"""
        if self.is_expired():
            return False
        if self.max_uses is not None and self.used_count >= self.max_uses:
            return False
        return True
    
    def use(self) -> None:
        """Mark the promotion as used"""
        if not self.can_be_used():
            raise ValueError("Promotion cannot be used")
        self.used_count += 1
    
    def set_max_uses(self, max_uses: int) -> None:
        """Set the maximum number of uses for this promotion"""
        if max_uses <= 0:
            raise ValueError("Max uses must be positive")
        self.max_uses = max_uses
    
    def calculate_discount(self, purchase_amount: Union[float, Money]) -> Money:
        """Calculate the discount amount for a given purchase"""
        amount = Money(purchase_amount) if isinstance(purchase_amount, (float, int)) else purchase_amount
        return amount.multiply(self.discount_percent / 100)
    
    def extend_validity(self, days: int) -> None:
        """Extend the promotion validity by a number of days"""
        if days <= 0:
            raise ValueError("Days to extend must be positive")
        from datetime import timedelta
        self.valid_until = self.valid_until + timedelta(days=days)
