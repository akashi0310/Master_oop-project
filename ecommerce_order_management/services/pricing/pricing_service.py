from typing import List
from ecommerce_order_management.domain.models.order import Order
from ecommerce_order_management.domain.models.customer import Customer
from ecommerce_order_management.domain.models.product import Product
from ecommerce_order_management.domain.models.promotion import Promotion
from ecommerce_order_management.domain.value_objects.money import Money
import datetime

class DiscountStrategy:
    def apply_discount(self, order: Order, customer: Customer, products: dict[str, Product], promotions: dict[str, Promotion]) -> Money:
        raise NotImplementedError

class PricingService:
    def __init__(self, discount_strategies: List[DiscountStrategy]):
        self.discount_strategies = discount_strategies

    def calculate_total(self, order: Order, customer: Customer, products: dict[str, Product], promotions: dict[str, Promotion]) -> Money:
        subtotal = sum(item.quantity * item.unit_price.amount for item in order.items)
        current_total = Money(subtotal, "USD")

        for strategy in self.discount_strategies:
            current_total = strategy.apply_discount(order, customer, products, promotions)

        return current_total