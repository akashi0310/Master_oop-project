import datetime
from typing import List
from ecommerce_order_management.domain.models.order_item import OrderItem
from ecommerce_order_management.domain.models.customer import CustomerId
from ecommerce_order_management.domain.value_objects.money import Money
from ecommerce_order_management.domain.enums.order_status import OrderStatus

class OrderId(str):
    pass

class Order:
    def __init__(self, order_id: OrderId, customer_id: CustomerId, items: List[OrderItem], status: OrderStatus, created_at: datetime.datetime, total_price: Money, shipping_cost: Money):
        if not isinstance(order_id, OrderId) or not order_id:
            raise ValueError("Order ID must be a non-empty string.")
        if not isinstance(customer_id, CustomerId) or not customer_id:
            raise ValueError("Customer ID must be a non-empty string.")
        if not isinstance(items, list) or not all(isinstance(item, OrderItem) for item in items):
            raise ValueError("Items must be a list of OrderItem objects.")
        if not isinstance(status, OrderStatus):
            raise ValueError("Invalid order status.")
        if not isinstance(created_at, datetime.datetime):
            raise ValueError("Created at must be a datetime object.")
        if not isinstance(total_price, Money) or total_price.amount < 0:
            raise ValueError("Total price must be a Money object with a non-negative amount.")
        if not isinstance(shipping_cost, Money) or shipping_cost.amount < 0:
            raise ValueError("Shipping cost must be a Money object with a non-negative amount.")

        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
        self.status = status
        self.created_at = created_at
        self.total_price = total_price
        self.shipping_cost = shipping_cost
        self.tracking_number: str | None = None
        self.payment_method: str | None = None