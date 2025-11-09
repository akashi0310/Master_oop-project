import datetime
from ecommerce_order_management.domain.value_objects.money import Money


class PromoId(str):
    pass

class Promotion:
    def __init__(self, promo_id: PromoId, code: str, discount_percent: float, min_purchase: Money, valid_until: datetime.datetime, category: str):
        if not isinstance(promo_id, PromoId) or not promo_id:
            raise ValueError("Promotion ID must be a non-empty string.")
        if not isinstance(code, str) or not code:
            raise ValueError("Promotion code must be a non-empty string.")
        if not isinstance(discount_percent, (int, float)) or not (0 < discount_percent <= 100):
            raise ValueError("Discount percent must be between 0 and 100.")
        if not isinstance(min_purchase, Money) or min_purchase.amount < 0:
            raise ValueError("Minimum purchase must be a Money object with a non-negative amount.")
        if not isinstance(valid_until, datetime.datetime):
            raise ValueError("Valid until must be a datetime object.")
        if not isinstance(category, str) or not category:
            raise ValueError("Category must be a non-empty string.")

        self.promo_id = promo_id
        self.code = code
        self.discount_percent = discount_percent
        self.min_purchase = min_purchase
        self.valid_until = valid_until
        self.category = category
        self.used_count: int = 0