import unittest
import datetime
from ecommerce_order_management.domain.models.promotion import Promotion, PromoId
from ecommerce_order_management.domain.value_objects.money import Money


class TestPromotion(unittest.TestCase):

    def test_promotion_creation_valid(self):
        promo = Promotion(
            promo_id=PromoId("PROMO001"),
            code="SUMMER20",
            discount_percent=20.0,
            min_purchase=Money(50.00),
            valid_until=datetime.datetime(2025, 8, 31),
            category="all"
        )
        self.assertEqual(promo.promo_id, "PROMO001")
        self.assertEqual(promo.code, "SUMMER20")
        self.assertEqual(promo.discount_percent, 20.0)
        self.assertEqual(promo.min_purchase, Money(50.00))
        self.assertEqual(promo.valid_until, datetime.datetime(2025, 8, 31))
        self.assertEqual(promo.category, "all")
        self.assertEqual(promo.used_count, 0)

    def test_promotion_creation_invalid_empty_promo_id(self):
        with self.assertRaisesRegex(ValueError, "Promotion ID must be a non-empty string."):
            Promotion(
                promo_id=PromoId(""),
                code="SUMMER20",
                discount_percent=20.0,
                min_purchase=Money(50.00),
                valid_until=datetime.datetime(2025, 8, 31),
                category="all"
            )

    def test_promotion_creation_invalid_empty_code(self):
        with self.assertRaisesRegex(ValueError, "Promotion code must be a non-empty string."):
            Promotion(
                promo_id=PromoId("PROMO001"),
                code="",
                discount_percent=20.0,
                min_purchase=Money(50.00),
                valid_until=datetime.datetime(2025, 8, 31),
                category="all"
            )

    def test_promotion_creation_invalid_discount_percent_too_low(self):
        with self.assertRaisesRegex(ValueError, "Discount percent must be between 0 and 100."):
            Promotion(
                promo_id=PromoId("PROMO001"),
                code="SUMMER20",
                discount_percent=0.0,
                min_purchase=Money(50.00),
                valid_until=datetime.datetime(2025, 8, 31),
                category="all"
            )

    def test_promotion_creation_invalid_discount_percent_too_high(self):
        with self.assertRaisesRegex(ValueError, "Discount percent must be between 0 and 100."):
            Promotion(
                promo_id=PromoId("PROMO001"),
                code="SUMMER20",
                discount_percent=101.0,
                min_purchase=Money(50.00),
                valid_until=datetime.datetime(2025, 8, 31),
                category="all"
            )

    def test_promotion_creation_invalid_min_purchase_negative(self):
        with self.assertRaisesRegex(ValueError, "Minimum purchase must be a Money object with a non-negative amount."):
            Promotion(
                promo_id=PromoId("PROMO001"),
                code="SUMMER20",
                discount_percent=20.0,
                min_purchase=Money(-10.00),
                valid_until=datetime.datetime(2025, 8, 31),
                category="all"
            )

    def test_promotion_creation_invalid_valid_until_type(self):
        with self.assertRaisesRegex(ValueError, "Valid until must be a datetime object."):
            Promotion(
                promo_id=PromoId("PROMO001"),
                code="SUMMER20",
                discount_percent=20.0,
                min_purchase=Money(50.00),
                valid_until="2025-08-31",  # should be datetime
                category="all"
            )

    def test_promotion_creation_invalid_empty_category(self):
        with self.assertRaisesRegex(ValueError, "Category must be a non-empty string."):
            Promotion(
                promo_id=PromoId("PROMO001"),
                code="SUMMER20",
                discount_percent=20.0,
                min_purchase=Money(50.00),
                valid_until=datetime.datetime(2025, 8, 31),
                category=""
            )


if __name__ == "__main__":
    unittest.main()
