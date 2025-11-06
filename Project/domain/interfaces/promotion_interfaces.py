from abc import ABC, abstractmethod
from typing import Union
from datetime import datetime
from ..value_objects.money import Money


class PromotionValidator(ABC):
    """Interface for promotion validation"""
    
    @abstractmethod
    def validate(self, promo_id: int, code: str, discount_percent: float, 
                min_purchase: Union[float, Money], valid_until: datetime, 
                category: str) -> None:
        """Validate promotion parameters"""
        pass


class DiscountCalculator(ABC):
    """Interface for discount calculation"""
    
    @abstractmethod
    def calculate_discount(self, discount_percent: float, purchase_amount: Union[float, Money]) -> Money:
        """Calculate discount amount"""
        pass


class PromotionUsageTracker(ABC):
    """Interface for tracking promotion usage"""
    
    @abstractmethod
    def can_be_used(self, used_count: int, max_uses: int) -> bool:
        """Check if promotion can still be used"""
        pass
    
    @abstractmethod
    def use(self, used_count: int) -> int:
        """Mark promotion as used and return new count"""
        pass


class PromotionValidityManager(ABC):
    """Interface for managing promotion validity"""
    
    @abstractmethod
    def is_valid(self, valid_until: datetime) -> bool:
        """Check if promotion is still valid"""
        pass
    
    @abstractmethod
    def extend_validity(self, valid_until: datetime, days: int) -> datetime:
        """Extend promotion validity"""
        pass


class PromotionEligibilityChecker(ABC):
    """Interface for checking promotion eligibility"""
    
    @abstractmethod
    def is_applicable_to_category(self, promotion_category: str, product_category: str) -> bool:
        """Check if promotion applies to a specific product category"""
        pass
    
    @abstractmethod
    def meets_minimum_purchase(self, min_purchase: Money, purchase_amount: Union[float, Money]) -> bool:
        """Check if purchase amount meets minimum requirement"""
        pass