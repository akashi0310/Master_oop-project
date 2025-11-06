from typing import Union, Optional
from datetime import datetime
from domain.value_objects.money import Money
from domain.interfaces.promotion_interfaces import (
    PromotionValidator, DiscountCalculator, PromotionUsageTracker,
    PromotionValidityManager, PromotionEligibilityChecker
)


class Promotion:
    """
    Refactored Promotion class following SOLID principles.
    
    This class now follows the Single Responsibility Principle by delegating
    specific tasks to specialized components through dependency injection.
    """
    
    def __init__(
        self,
        promo_id: int,
        code: str,
        discount_percent: float,
        min_purchase: Union[float, Money],
        valid_until: datetime,
        category: str = "all",
        validator: Optional[PromotionValidator] = None,
        discount_calculator: Optional[DiscountCalculator] = None,
        usage_tracker: Optional[PromotionUsageTracker] = None,
        validity_manager: Optional[PromotionValidityManager] = None,
        eligibility_checker: Optional[PromotionEligibilityChecker] = None
    ):
        # Use dependency injection with default implementations
        self._validator = validator
        self._discount_calculator = discount_calculator
        self._usage_tracker = usage_tracker
        self._validity_manager = validity_manager
        self._eligibility_checker = eligibility_checker
        
        # Validate parameters if validator is provided
        if self._validator:
            self._validator.validate(promo_id, code, discount_percent, min_purchase, valid_until, category)
        
        # Set properties
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
        if self._validity_manager:
            return self._validity_manager.is_valid(self.valid_until)
        # Fallback to default behavior
        return datetime.now() < self.valid_until
    
    def is_expired(self) -> bool:
        """Check if the promotion has expired"""
        return not self.is_valid()
    
    def is_applicable_to_category(self, product_category: str) -> bool:
        """Check if the promotion applies to a specific product category"""
        if self._eligibility_checker:
            return self._eligibility_checker.is_applicable_to_category(self.category, product_category.lower())
        # Fallback to default behavior
        return self.category == "all" or self.category == product_category.lower()
    
    def meets_minimum_purchase(self, purchase_amount: Union[float, Money]) -> bool:
        """Check if the purchase amount meets the minimum requirement"""
        if self._eligibility_checker:
            return self._eligibility_checker.meets_minimum_purchase(self.min_purchase, purchase_amount)
        # Fallback to default behavior
        amount = Money(purchase_amount) if isinstance(purchase_amount, (float, int)) else purchase_amount
        return amount.is_greater_than(self.min_purchase) or amount.amount == self.min_purchase.amount
    
    def can_be_used(self) -> bool:
        """Check if the promotion can still be used"""
        if self.is_expired():
            return False
        if self._usage_tracker:
            return self._usage_tracker.can_be_used(self.used_count, self.max_uses)
        # Fallback to default behavior
        return self.max_uses is None or self.used_count < self.max_uses
    
    def use(self) -> None:
        """Mark the promotion as used"""
        if not self.can_be_used():
            raise ValueError("Promotion cannot be used")
        
        if self._usage_tracker:
            self.used_count = self._usage_tracker.use(self.used_count)
        else:
            # Fallback to default behavior
            self.used_count += 1
    
    def set_max_uses(self, max_uses: int) -> None:
        """Set the maximum number of uses for this promotion"""
        if max_uses <= 0:
            raise ValueError("Max uses must be positive")
        self.max_uses = max_uses
    
    def calculate_discount(self, purchase_amount: Union[float, Money]) -> Money:
        """Calculate the discount amount for a given purchase"""
        if self._discount_calculator:
            return self._discount_calculator.calculate_discount(self.discount_percent, purchase_amount)
        # Fallback to default behavior
        amount = Money(purchase_amount) if isinstance(purchase_amount, (float, int)) else purchase_amount
        return amount.multiply(self.discount_percent / 100)
    
    def extend_validity(self, days: int) -> None:
        """Extend the promotion validity by a number of days"""
        if self._validity_manager:
            self.valid_until = self._validity_manager.extend_validity(self.valid_until, days)
        else:
            # Fallback to default behavior
            if days <= 0:
                raise ValueError("Days to extend must be positive")
            from datetime import timedelta
            self.valid_until = self.valid_until + timedelta(days=days)
