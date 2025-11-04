import random
from storage import database
from services.notification_service import NotificationService
from services.supplier_reorder_service import SupplierReorderService
from services.inventory_service import log_inventory_change
from services.shipment_service import ShipmentService


class OrderService:
    def __init__(self):
        self.notification_service = NotificationService()
        self.reorder_service = SupplierReorderService()
        self.shipment_service = ShipmentService()

    # -------------------- Core Retrieval --------------------

    def get_order(self, order_id):
        """Retrieve a single order."""
        return database.orders.get(order_id)

    def get_customer_orders(self, customer_id):
        """Return all orders for a given customer."""
        return [o for o in database.orders.values() if o.customer_id == customer_id]

    # -------------------- Updates & Status --------------------

    def update_order_status(self, order_id, new_status):
        """Update the order status and trigger notifications/shipment if needed."""
        order = database.orders.get(order_id)
        if not order:
            print("Order not found")
            return None

        old_status = order.status
        order.status = new_status

        customer = database.customers.get(order.customer_id)
        if customer:
            self.notification_service.notify_status_update(customer, order_id, new_status)

        if new_status == 'shipped' and not order.tracking_number:
            order.tracking_number = f"TRACK{order_id}{random.randint(1000, 9999)}"
            self.shipment_service.create_shipment(order_id, order.tracking_number)

        return order

    # -------------------- Discounts --------------------

    def apply_additional_discount(self, order_id, discount_percent, reason):
        """Apply a manual discount to a pending order."""
        order = database.orders.get(order_id)
        if not order:
            print("Order not found")
            return None

        if order.status != 'pending':
            print("Can only apply discount to pending orders")
            return None

        order.total_price *= (1 - discount_percent / 100)
        print(f"Applied {discount_percent}% discount to Order {order_id}. Reason: {reason}")
        return order

    # -------------------- Cancellation --------------------

    def cancel_order(self, order_id, reason):
        """Cancel an order, restore stock, and notify customer."""
        order = database.orders.get(order_id)
        if not order:
            print("Order not found")
            return False

        if order.status in ['shipped', 'delivered']:
            print(f"Cannot cancel order in {order.status} status")
            return False

        # Restore stock
        for item in order.items:
            product = database.products.get(item.product_id)
            if product:
                product.quantity_available += item.quantity
                log_inventory_change(item.product_id, item.quantity, f"cancel_order_{order_id}")

        # Update order
        order.status = 'cancelled'

        # Notify customer
        customer = database.customers.get(order.customer_id)
        if customer:
            self.notification_service.notify_order_cancelled(customer, order_id, reason)

        return True
