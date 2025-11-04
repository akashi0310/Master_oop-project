class Order:
    def __init__(self, order_id, customer_id, items, status, created_at, total_price, shipping_cost):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
        self.status = status
        self.created_at = created_at
        self.total_price = total_price
        self.shipping_cost = shipping_cost
        self.tracking_number = None
        self.payment_method = None
