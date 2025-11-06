import unittest
import sys
import os
from datetime import datetime, timedelta

# Add the Project directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from domain.value_objects.money import Money
from domain.models.promotion import Promotion
from services.promotion_factory import PromotionFactory
from services.promotion_service import (
    DefaultPromotionValidator, PercentageDiscountCalculator,
    BasicPromotionUsageTracker, StandardPromotionValidityManager,
    CategoryBasedEligibilityChecker
)


class TestPromotionRefactored(unittest.TestCase):
    """Test cases for the refactored Promotion class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.future_date = datetime.now() + timedelta(days=30)
        self.past_date = datetime.now() - timedelta(days=1)
        
    def test_promotion_creation_with_factory(self):
        """Test creating a promotion using the factory"""
        promotion = PromotionFactory.create_percentage_discount_promotion(
            promo_id=1,
            code="TEST10",
            discount_percent=10.0,
            min_purchase=Money(100.0),
            valid_until=self.future_date,
            category="electronics"
        )
        
        self.assertEqual(promotion.promo_id, 1)
        self.assertEqual(promotion.code, "TEST10")
        self.assertEqual(promotion.discount_percent, 10.0)
        self.assertEqual(promotion.min_purchase.amount, 100.0)
        self.assertEqual(promotion.category, "electronics")
        self.assertTrue(promotion.is_valid())
        
    def test_promotion_validation(self):
        """Test promotion validation"""
        # Test invalid promo_id
        with self.assertRaises(ValueError):
            PromotionFactory.create_percentage_discount_promotion(
                promo_id=-1,
                code="TEST10",
                discount_percent=10.0,
                min_purchase=Money(100.0),
                valid_until=self.future_date
            )
        
        # Test invalid discount_percent
        with self.assertRaises(ValueError):
            PromotionFactory.create_percentage_discount_promotion(
                promo_id=1,
                code="TEST10",
                discount_percent=110.0,
                min_purchase=Money(100.0),
                valid_until=self.future_date
            )
        
        # Test empty code
        with self.assertRaises(ValueError):
            PromotionFactory.create_percentage_discount_promotion(
                promo_id=1,
                code="",
                discount_percent=10.0,
                min_purchase=Money(100.0),
                valid_until=self.future_date
            )
    
    def test_promotion_validity(self):
        """Test promotion validity checking"""
        # Valid promotion
        valid_promo = PromotionFactory.create_percentage_discount_promotion(
            promo_id=1,
            code="VALID10",
            discount_percent=10.0,
            min_purchase=Money(100.0),
            valid_until=self.future_date
        )
        self.assertTrue(valid_promo.is_valid())
        self.assertFalse(valid_promo.is_expired())
        
        # Expired promotion
        expired_promo = PromotionFactory.create_percentage_discount_promotion(
            promo_id=2,
            code="EXPIRED10",
            discount_percent=10.0,
            min_purchase=Money(100.0),
            valid_until=self.past_date
        )
        self.assertFalse(expired_promo.is_valid())
        self.assertTrue(expired_promo.is_expired())
    
    def test_promotion_category_eligibility(self):
        """Test promotion category eligibility"""
        promo = PromotionFactory.create_percentage_discount_promotion(
            promo_id=1,
            code="ELECT10",
            discount_percent=10.0,
            min_purchase=Money(100.0),
            valid_until=self.future_date,
            category="electronics"
        )
        
        # Should apply to electronics
        self.assertTrue(promo.is_applicable_to_category("electronics"))
        
        # Should not apply to books
        self.assertFalse(promo.is_applicable_to_category("books"))
        
        # "all" category should apply to everything
        all_promo = PromotionFactory.create_percentage_discount_promotion(
            promo_id=2,
            code="ALL10",
            discount_percent=10.0,
            min_purchase=Money(100.0),
            valid_until=self.future_date,
            category="all"
        )
        self.assertTrue(all_promo.is_applicable_to_category("electronics"))
        self.assertTrue(all_promo.is_applicable_to_category("books"))
    
    def test_minimum_purchase_requirement(self):
        """Test minimum purchase requirement"""
        promo = PromotionFactory.create_percentage_discount_promotion(
            promo_id=1,
            code="MIN100",
            discount_percent=10.0,
            min_purchase=Money(100.0),
            valid_until=self.future_date
        )
        
        # Should meet minimum purchase
        self.assertTrue(promo.meets_minimum_purchase(Money(100.0)))
        self.assertTrue(promo.meets_minimum_purchase(Money(150.0)))
        
        # Should not meet minimum purchase
        self.assertFalse(promo.meets_minimum_purchase(Money(99.99)))
    
    def test_usage_tracking(self):
        """Test promotion usage tracking"""
        promo = PromotionFactory.create_percentage_discount_promotion(
            promo_id=1,
            code="LIMITED",
            discount_percent=10.0,
            min_purchase=Money(100.0),
            valid_until=self.future_date
        )
        
        # Set max uses
        promo.set_max_uses(3)
        
        # Should be usable initially
        self.assertTrue(promo.can_be_used())
        
        # Use it 3 times
        promo.use()
        promo.use()
        promo.use()
        
        # Should no longer be usable
        self.assertFalse(promo.can_be_used())
        
        # Using it again should raise an error
        with self.assertRaises(ValueError):
            promo.use()
    
    def test_discount_calculation(self):
        """Test discount calculation"""
        promo = PromotionFactory.create_percentage_discount_promotion(
            promo_id=1,
            code="DISCOUNT10",
            discount_percent=10.0,
            min_purchase=Money(100.0),
            valid_until=self.future_date
        )
        
        # Calculate discount on $100 purchase
        discount = promo.calculate_discount(Money(100.0))
        self.assertEqual(discount.amount, 10.0)
        
        # Calculate discount on $50 purchase
        discount = promo.calculate_discount(Money(50.0))
        self.assertEqual(discount.amount, 5.0)
    
    def test_extend_validity(self):
        """Test extending promotion validity"""
        original_date = datetime.now() + timedelta(days=10)
        promo = PromotionFactory.create_percentage_discount_promotion(
            promo_id=1,
            code="EXTEND",
            discount_percent=10.0,
            min_purchase=Money(100.0),
            valid_until=original_date
        )
        
        # Extend by 5 days
        promo.extend_validity(5)
        expected_date = original_date + timedelta(days=5)
        self.assertEqual(promo.valid_until, expected_date)
        
        # Try to extend by negative days (should raise error)
        with self.assertRaises(ValueError):
            promo.extend_validity(-5)
    
    def test_custom_implementations(self):
        """Test using custom implementations of interfaces"""
        # Create custom implementations
        class CustomValidator(DefaultPromotionValidator):
            def validate(self, promo_id, code, discount_percent, min_purchase, valid_until, category):
                # Only allow promo codes that start with "CUSTOM"
                if not code.startswith("CUSTOM"):
                    raise ValueError("Only custom promo codes allowed")
                super().validate(promo_id, code, discount_percent, min_purchase, valid_until, category)
        
        # Test with custom validator
        with self.assertRaises(ValueError):
            PromotionFactory.create_promotion(
                promo_id=1,
                code="REGULAR",
                discount_percent=10.0,
                min_purchase=Money(100.0),
                valid_until=self.future_date,
                validator=CustomValidator()
            )
        
        # Should work with custom validator
        promo = PromotionFactory.create_promotion(
            promo_id=1,
            code="CUSTOM10",
            discount_percent=10.0,
            min_purchase=Money(100.0),
            valid_until=self.future_date,
            validator=CustomValidator()
        )
        self.assertEqual(promo.code, "CUSTOM10")


if __name__ == "__main__":
    unittest.main()