from ecommerce_order_management.domain.models.customer import Customer
from ecommerce_order_management.domain.models.order import Order
from ecommerce_order_management.domain.models.product import Product, ProductId
from ecommerce_order_management.domain.models.supplier import Supplier, SupplierId
from typing import Dict, List

class NotificationService:
    def send_order_confirmation(self, customer: Customer, order: Order) -> None:
        print(f"To: {customer.email}: Order {order.order_id} confirmed! Total: ${order.total_price.amount:.2f}")
        if customer.phone:
            print(f"SMS to {customer.phone}: Order {order.order_id} confirmed")

    def send_order_status_update(self, customer: Customer, order: Order) -> None:
        print(f"To: {customer.email}: Order {order.order_id} status changed to {order.status}")

    def notify_supplier_reorder(self, product: Product, supplier: Supplier) -> None:
        print(f"Email to {supplier.email}: Low stock alert for {product.name}")

    def send_marketing_email(self, customer: Customer, message: str) -> None:
        print(f"Email to {customer.email}: {message}")

    def send_cancellation_notification(self, customer: Customer, order: Order, reason: str) -> None:
        print(f"To: {customer.email}: Order {order.order_id} has been cancelled. Reason: {reason}")