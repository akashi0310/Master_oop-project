from storage import database
from models.customer import Customer

from storage import database

class CustomerService:
    @staticmethod
    def add_customer(customer_id, name, email, tier, phone, address):
        database.customers[customer_id] = Customer(customer_id, name, email, tier, phone, address, 0)

    @staticmethod
    def get_customer(customer_id):
        return database.customers.get(customer_id)

    @staticmethod
    def get_customer_lifetime_value(customer_id):
        """Calculate the total value of all completed (non-cancelled) orders."""
        customer = database.customers.get(customer_id)
        if not customer:
            return 0

        total_value = 0
        for order_id in customer.order_history:
            order = database.orders.get(order_id)
            if order and order.status != 'cancelled':
                total_value += order.total_price
        return total_value
