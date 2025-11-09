import datetime
from ecommerce_order_management.services.pricing.pricing_service import DiscountStrategy
from ecommerce_order_management.domain.models.order import Order
from ecommerce_order_management.domain.models.customer import Customer
from ecommerce_order_management.domain.models.product import Product
from ecommerce_order_management.domain.models.promotion import Promotion, PromoId
from ecommerce_order_management.domain.value_objects.money import Money
from typing import Dict

class PromotionalDiscount(DiscountStrategy):
    def apply_discount(self, order: Order, customer: Customer, products: Dict[str, Product], promotions: Dict[PromoId, Promotion]) -> Money:
        promo_code = order.promo_code # Assuming order has a promo_code attribute
        promo_discount_amount = 0.0

        if promo_code:
            promo = promotions.get(promo_code)
            if promo:
                if datetime.datetime.now() < promo.valid_until:
                    current_total = order.total_price.amount if order.total_price else sum(item.quantity * item.unit_price.amount for item in order.items)
                    if current_total >= promo.min_purchase.amount:
                        applicable = False
                        for item in order.items:
                            product = products.get(item.product_id)
                            if product and (promo.category == 'all' or product.category == promo.category):
                                applicable = True
                                break
                        if applicable:
                            promo_discount_amount = current_total * (promo.discount_percent / 100)
                            promo.used_count += 1 # This modifies the global promotions dict, which might be an issue if not handled carefully

        current_total = order.total_price.amount if order.total_price else sum(item.quantity * item.unit_price.amount for item in order.items)
        return Money(current_total - promo_discount_amount, "USD")