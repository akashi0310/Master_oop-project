from ecommerce_order_management.services.pricing.pricing_service import DiscountStrategy
from ecommerce_order_management.domain.models.order import Order
from ecommerce_order_management.domain.models.customer import Customer
from ecommerce_order_management.domain.models.product import Product
from ecommerce_order_management.domain.models.promotion import Promotion
from ecommerce_order_management.domain.value_objects.money import Money
from typing import Dict

class MembershipDiscount(DiscountStrategy):
    def apply_discount(self, order: Order, customer: Customer, products: Dict[str, Product], promotions: Dict[str, Promotion]) -> Money:
        discount_rate = 0.0
        if customer.membership_tier == 'gold':
            discount_rate = 0.15
        elif customer.membership_tier == 'silver':
            discount_rate = 0.07
        elif customer.membership_tier == 'bronze':
            discount_rate = 0.03
        
        current_total = order.total_price.amount if order.total_price else sum(item.quantity * item.unit_price.amount for item in order.items)
        discount_amount = current_total * discount_rate
        return Money(current_total - discount_amount, "USD")