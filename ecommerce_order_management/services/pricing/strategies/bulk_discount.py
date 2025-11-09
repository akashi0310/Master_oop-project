from ecommerce_order_management.services.pricing.pricing_service import DiscountStrategy
from ecommerce_order_management.domain.models.order import Order
from ecommerce_order_management.domain.models.customer import Customer
from ecommerce_order_management.domain.models.product import Product
from ecommerce_order_management.domain.models.promotion import Promotion
from ecommerce_order_management.domain.value_objects.money import Money
from typing import Dict

class BulkDiscount(DiscountStrategy):
    def apply_discount(self, order: Order, customer: Customer, products: Dict[str, Product], promotions: Dict[str, Promotion]) -> Money:
        total_items = sum(item.quantity for item in order.items)
        bulk_discount_rate = 0.0

        if total_items >= 10:
            bulk_discount_rate = 0.05
        elif total_items >= 5:
            bulk_discount_rate = 0.02
        
        current_total = order.total_price.amount if order.total_price else sum(item.quantity * item.unit_price.amount for item in order.items)
        discount_amount = current_total * bulk_discount_rate
        return Money(current_total - discount_amount, "USD")