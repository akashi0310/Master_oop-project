from ecommerce_order_management.domain.models.customer import Customer, CustomerId
from ecommerce_order_management.domain.models.order import Order
from ecommerce_order_management.domain.value_objects.address import Address
from ecommerce_order_management.domain.value_objects.email import Email
from typing import Dict, List

class CustomerService:
    def __init__(self, customers: Dict[CustomerId, Customer], orders: Dict[int, Order]):
        self.customers = customers
        self.orders = orders

    def add_customer(self, customer_id: CustomerId, name: str, email: Email, tier: str, phone: str, address: Address) -> None:
        self.customers[customer_id] = Customer(customer_id, name, email, tier, phone, address, 0)

    def get_customer(self, customer_id: CustomerId) -> Customer | None:
        return self.customers.get(customer_id)

    def get_customer_lifetime_value(self, customer_id: CustomerId) -> float:
        customer = self.customers.get(customer_id)
        if not customer:
            return 0.0

        total_value = 0.0
        for order_id in customer.order_history:
            order = self.orders.get(order_id)
            if order and order.status != 'cancelled':
                total_value += order.total_price.amount # Assuming Money object has .amount
        return total_value

    def upgrade_customer_membership(self, customer_id: CustomerId) -> bool:
        customer = self.customers.get(customer_id)
        if not customer:
            return False

        lifetime_value = self.get_customer_lifetime_value(customer_id)

        if lifetime_value >= 1000 and customer.membership_tier != 'gold':
            customer.membership_tier = 'gold'
            return True
        elif lifetime_value >= 500 and customer.membership_tier == 'standard':
            customer.membership_tier = 'silver'
            return True
        elif lifetime_value >= 200 and customer.membership_tier == 'standard':
            customer.membership_tier = 'bronze'
            return True
        return False

    def get_customer_orders(self, customer_id: CustomerId) -> List[Order]:
        customer_orders = []
        for order in self.orders.values():
            if order.customer_id == customer_id:
                customer_orders.append(order)
        return customer_orders