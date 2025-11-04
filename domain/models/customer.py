class Customer:
    def __init__(self, customer_id, name, email, membership_tier, phone, address, loyalty_points=0):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.membership_tier = membership_tier
        self.phone = phone
        self.address = address
        self.loyalty_points = loyalty_points
        self.order_history = []

    def add_loyalty_points(self, points):
        self.loyalty_points += points
