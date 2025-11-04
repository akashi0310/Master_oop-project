class NotificationService:
    def notify_order_confirmation(self, customer, order_id, total):
        print(f"Email to {customer.email}: Order {order_id} confirmed! Total: ${total:.2f}")
        if customer.phone:
            print(f"SMS to {customer.phone}: Order {order_id} confirmed")

    def notify_status_update(self, customer, order_id, new_status):
        print(f"Email to {customer.email}: Order {order_id} status changed to {new_status}")

    def notify_order_cancelled(self, customer, order_id, reason):
        print(f"Email to {customer.email}: Order {order_id} has been cancelled. Reason: {reason}")
