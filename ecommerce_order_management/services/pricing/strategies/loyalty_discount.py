from ecommerce_order_management.services.pricing.pricing_service import DiscountStrategy
from ecommerce_order_management.domain.models.order import Order
from ecommerce_order_management.domain.models.customer import Customer
from ecommerce_order_management.domain.models.product import Product
from ecommerce_order_management.domain.models.promotion import Promotion
from ecommerce_order_management.domain.value_objects.money import Money
from typing import Dict

class LoyaltyDiscount(DiscountStrategy):
    def apply_discount(self, order: Order, customer: Customer, products: Dict[str, Product], promotions: Dict[str, Promotion]) -> Money:
        loyalty_discount_amount = 0.0
        current_total = order.total_price.amount if order.total_price else sum(item.quantity * item.unit_price.amount for item in order.items)

        if customer.loyalty_points >= 100:
            loyalty_discount_amount = min(current_total * 0.1, customer.loyalty_points * 0.01)
            customer.loyalty_points -= int(loyalty_discount_amount * 100) # Deduct points

        return Money(current_total - loyalty_discount_amount, "USD")