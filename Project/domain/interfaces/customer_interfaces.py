from abc import ABC, abstractmethod
from typing import Protocol
from ..value_objects.email import Email
from ..value_objects.address import Address
from ..enums.membership_tier import MembershipTier


class CustomerInfo(Protocol):
    """Protocol for basic customer information"""
    customer_id: int
    name: str
    email: Email
    phone: str | None
    address: Address | None


class LoyaltyOperations(Protocol):
    """Protocol for loyalty points operations"""
    def add_loyalty_points(self, points: int) -> None:
        ...
    
    def redeem_loyalty_points(self, points: int) -> bool:
        ...
    
    @property
    def loyalty_points(self) -> int:
        ...


class MembershipOperations(Protocol):
    """Protocol for membership operations"""
    def upgrade_membership(self, new_tier: MembershipTier) -> None:
        ...
    
    def get_membership_discount_rate(self) -> float:
        ...
    
    def get_shipping_discount_rate(self) -> float:
        ...
    
    def can_place_order(self) -> bool:
        ...
    
    @property
    def membership_tier(self) -> MembershipTier:
        ...


class OrderHistoryOperations(Protocol):
    """Protocol for order history operations"""
    def add_order_to_history(self, order_id: int) -> None:
        ...
    
    @property
    def order_history(self) -> list[int]:
        ...


class CustomerValidator(ABC):
    """Abstract base class for customer validation"""
    
    @abstractmethod
    def validate_customer_data(self, customer_id: int, name: str, loyalty_points: int) -> None:
        """Validate basic customer data"""
        pass