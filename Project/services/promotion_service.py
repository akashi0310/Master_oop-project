from typing import Union
from datetime import datetime, timedelta
from domain.value_objects.money import Money
from domain.interfaces.promotion_interfaces import (
    PromotionValidator, DiscountCalculator, PromotionUsageTracker,
    PromotionValidityManager, PromotionEligibilityChecker
)


class DefaultPromotionValidator(PromotionValidator):
    """Default implementation of promotion validation"""
    
    def validate(self, promo_id: int, code: str, discount_percent: float, 
                min_purchase: Union[float, Money], valid_until: datetime, 
                category: str) -> None:
        """Validate promotion parameters"""
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


class PercentageDiscountCalculator(DiscountCalculator):
    """Implementation for percentage-based discount calculation"""
    
    def calculate_discount(self, discount_percent: float, purchase_amount: Union[float, Money]) -> Money:
        """Calculate discount amount based on percentage"""
        amount = Money(purchase_amount) if isinstance(purchase_amount, (float, int)) else purchase_amount
        return amount.multiply(discount_percent / 100)


class BasicPromotionUsageTracker(PromotionUsageTracker):
    """Basic implementation for tracking promotion usage"""
    
    def can_be_used(self, used_count: int, max_uses: int) -> bool:
        """Check if promotion can still be used"""
        return max_uses is None or used_count < max_uses
    
    def use(self, used_count: int) -> int:
        """Mark promotion as used and return new count"""
        return used_count + 1


class StandardPromotionValidityManager(PromotionValidityManager):
    """Standard implementation for managing promotion validity"""
    
    def is_valid(self, valid_until: datetime) -> bool:
        """Check if promotion is still valid"""
        return datetime.now() < valid_until
    
    def extend_validity(self, valid_until: datetime, days: int) -> datetime:
        """Extend promotion validity"""
        if days <= 0:
            raise ValueError("Days to extend must be positive")
        return valid_until + timedelta(days=days)


class CategoryBasedEligibilityChecker(PromotionEligibilityChecker):
    """Implementation for category-based eligibility checking"""
    
    def is_applicable_to_category(self, promotion_category: str, product_category: str) -> bool:
        """Check if promotion applies to a specific product category"""
        return promotion_category == "all" or promotion_category == product_category.lower()
    
    def meets_minimum_purchase(self, min_purchase: Money, purchase_amount: Union[float, Money]) -> bool:
        """Check if purchase amount meets minimum requirement"""
        amount = Money(purchase_amount) if isinstance(purchase_amount, (float, int)) else purchase_amount
        return amount.is_greater_than(min_purchase) or amount.amount == min_purchase.amount