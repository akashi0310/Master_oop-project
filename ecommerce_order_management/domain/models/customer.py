from typing import List
from ecommerce_order_management.domain.value_objects.address import Address
from ecommerce_order_management.domain.value_objects.email import Email
from ecommerce_order_management.domain.enums.membership_tier import MembershipTier

class CustomerId(str):
    pass

class Customer:
    def __init__(self, customer_id: CustomerId, name: str, email: Email, membership_tier: MembershipTier, phone: str, address: Address, loyalty_points: int):
        if not isinstance(customer_id, CustomerId) or not customer_id:
            raise ValueError("Customer ID must be a non-empty string.")
        if not isinstance(name, str) or not name:
            raise ValueError("Customer name must be a non-empty string.")
        if not isinstance(email, Email):
            raise ValueError("Email must be an Email object.")
        if not isinstance(membership_tier, MembershipTier):
            raise ValueError("Invalid membership tier.")
        if not isinstance(phone, str) or not phone:
            raise ValueError("Phone number must be a non-empty string.")
        if not isinstance(address, Address):
            raise ValueError("Address must be an Address object.")
        if not isinstance(loyalty_points, int) or loyalty_points < 0:
            raise ValueError("Loyalty points must be a non-negative integer.")

        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.membership_tier = membership_tier
        self.phone = phone
        self.address = address
        self.loyalty_points = loyalty_points
        self.order_history: List[str] = [] # Assuming order_id will be string