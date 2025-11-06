from typing import Union, Optional
from datetime import datetime
from domain.value_objects.money import Money
from domain.models.promotion import Promotion
from domain.interfaces.promotion_interfaces import (
    PromotionValidator, DiscountCalculator, PromotionUsageTracker,
    PromotionValidityManager, PromotionEligibilityChecker
)
from services.promotion_service import (
    DefaultPromotionValidator, PercentageDiscountCalculator,
    BasicPromotionUsageTracker, StandardPromotionValidityManager,
    CategoryBasedEligibilityChecker
)


class PromotionFactory:
    """
    Factory class for creating Promotion instances with default implementations.
    
    This follows the Dependency Inversion Principle by providing concrete
    implementations of the interfaces required by the Promotion class.
    """
    
    @staticmethod
    def create_promotion(
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
    ) -> Promotion:
        """
        Create a Promotion instance with default implementations if not provided.
        
        Args:
            promo_id: Unique identifier for the promotion
            code: Promotion code
            discount_percent: Discount percentage (0-100)
            min_purchase: Minimum purchase amount to qualify
            valid_until: Expiration date of the promotion
            category: Product category the promotion applies to
            validator: Optional custom validator implementation
            discount_calculator: Optional custom discount calculator
            usage_tracker: Optional custom usage tracker
            validity_manager: Optional custom validity manager
            eligibility_checker: Optional custom eligibility checker
            
        Returns:
            A configured Promotion instance
        """
        # Use default implementations if not provided
        validator = validator or DefaultPromotionValidator()
        discount_calculator = discount_calculator or PercentageDiscountCalculator()
        usage_tracker = usage_tracker or BasicPromotionUsageTracker()
        validity_manager = validity_manager or StandardPromotionValidityManager()
        eligibility_checker = eligibility_checker or CategoryBasedEligibilityChecker()
        
        return Promotion(
            promo_id=promo_id,
            code=code,
            discount_percent=discount_percent,
            min_purchase=min_purchase,
            valid_until=valid_until,
            category=category,
            validator=validator,
            discount_calculator=discount_calculator,
            usage_tracker=usage_tracker,
            validity_manager=validity_manager,
            eligibility_checker=eligibility_checker
        )
    
    @staticmethod
    def create_percentage_discount_promotion(
        promo_id: int,
        code: str,
        discount_percent: float,
        min_purchase: Union[float, Money],
        valid_until: datetime,
        category: str = "all"
    ) -> Promotion:
        """
        Convenience method for creating a standard percentage discount promotion.
        
        Args:
            promo_id: Unique identifier for the promotion
            code: Promotion code
            discount_percent: Discount percentage (0-100)
            min_purchase: Minimum purchase amount to qualify
            valid_until: Expiration date of the promotion
            category: Product category the promotion applies to
            
        Returns:
            A configured Promotion instance with percentage discount
        """
        return PromotionFactory.create_promotion(
            promo_id=promo_id,
            code=code,
            discount_percent=discount_percent,
            min_purchase=min_purchase,
            valid_until=valid_until,
            category=category
        )