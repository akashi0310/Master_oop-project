from typing import Optional, Union, Dict
from domain.models import Customer
from domain.enums import MembershipTier
from domain.value_objects import Email, Address


class CustomerService:
    """
    Minimal CustomerService focused on essential operations.
    Stores customers in-memory and provides registration, loyalty, and membership features.
    """

    def __init__(self):
        self._customers: Dict[int, Customer] = {}
        self._next_id: int = 1

    def register_customer(
        self,
        name: str,
        email: Union[str, Email],
        address: Optional[Address] = None,
        membership_tier: Union[str, MembershipTier] = MembershipTier.STANDARD,
    ) -> Customer:
        """Register a new customer and return the created Customer."""
        customer_id = self._next_id
        self._next_id += 1
        customer = Customer(
            customer_id=customer_id,
            name=name,
            email=email,
            membership_tier=membership_tier,
            address=address,
        )
        self._customers[customer_id] = customer
        return customer

    def get_customer(self, customer_id: int) -> Optional[Customer]:
        """Get a customer by ID."""
        return self._customers.get(customer_id)

    def add_loyalty_points(self, customer_id: int, points: int) -> bool:
        """Add loyalty points to a customer's account."""
        customer = self.get_customer(customer_id)
        if not customer:
            return False
        customer.add_loyalty_points(points)
        return True

    def get_loyalty_points(self, customer_id: int) -> int:
        """Return customer's current loyalty points, or 0 if not found."""
        customer = self.get_customer(customer_id)
        return customer.loyalty_points if customer else 0

    def upgrade_membership(self, customer_id: int, new_tier: MembershipTier) -> Optional[Customer]:
        """Upgrade the customer's membership tier and return the updated customer."""
        customer = self.get_customer(customer_id)
        if not customer:
            return None
        customer.upgrade_membership(new_tier)
        return customer