from typing import Optional, Union
from ..value_objects.email import Email
from ..value_objects.address import Address
from ..enums.membership_tier import MembershipTier
from services.loyalty_points_manager import LoyaltyPointsManager
from services.membership_manager import MembershipManager
from services.order_history_manager import OrderHistoryManager
from services.customer_validator import DefaultCustomerValidator
from ..interfaces.customer_interfaces import (
    CustomerInfo,
    LoyaltyOperations,
    MembershipOperations,
    OrderHistoryOperations,
    CustomerValidator
)


class Customer(
    CustomerInfo,
    LoyaltyOperations,
    MembershipOperations,
    OrderHistoryOperations
):
    """
    Customer class that follows SOLID principles by delegating
    responsibilities to specialized components.
    """
    
    def __init__(
        self,
        customer_id: int,
        name: str,
        email: Union[str, Email],
        membership_tier: Union[str, MembershipTier],
        phone: Optional[str] = None,
        address: Optional[Union[str, Address]] = None,
        loyalty_points: int = 0,
        validator: Optional[CustomerValidator] = None
    ):
        # Use dependency injection for validation
        self._validator = validator or DefaultCustomerValidator()
        
        # Validate customer data
        self._validator.validate_customer_data(customer_id, name, loyalty_points)
        
        # Set basic customer information
        self.customer_id = customer_id
        self.name = name.strip()
        self.email = Email(email) if isinstance(email, str) else email
        self.phone = phone.strip() if phone else None
        self.address = Address.from_string(address) if isinstance(address, str) else address
        
        # Initialize specialized managers
        tier = MembershipTier(membership_tier.lower()) if isinstance(membership_tier, str) else membership_tier
        self._membership_manager = MembershipManager(tier)
        self._loyalty_manager = LoyaltyPointsManager(loyalty_points)
        self._order_history_manager = OrderHistoryManager()
    
    # Properties to access managed data
    @property
    def membership_tier(self) -> MembershipTier:
        """Get current membership tier"""
        return self._membership_manager.membership_tier
    
    @property
    def loyalty_points(self) -> int:
        """Get current loyalty points"""
        return self._loyalty_manager.points
    
    @property
    def order_history(self) -> list[int]:
        """Get a copy of the order history"""
        return self._order_history_manager.order_history
    
    # Loyalty operations
    def add_loyalty_points(self, points: int) -> None:
        """Add loyalty points to the customer's account"""
        self._loyalty_manager.add_points(points, self._membership_manager)
    
    def redeem_loyalty_points(self, points: int) -> bool:
        """Redeem loyalty points if available"""
        return self._loyalty_manager.redeem_points(points)
    
    # Membership operations
    def upgrade_membership(self, new_tier: MembershipTier) -> None:
        """Upgrade the customer's membership tier"""
        self._membership_manager.upgrade_membership(new_tier)
    
    def get_membership_discount_rate(self) -> float:
        """Get the discount rate for this customer's membership tier"""
        return self._membership_manager.get_discount_rate()
    
    def get_shipping_discount_rate(self) -> float:
        """Get the shipping discount rate for this customer's membership tier"""
        return self._membership_manager.get_shipping_discount_rate()
    
    def can_place_order(self) -> bool:
        """Check if customer can place orders"""
        return self._membership_manager.can_place_orders()
    
    # Order history operations
    def add_order_to_history(self, order_id: int) -> None:
        """Add an order ID to the customer's order history"""
        self._order_history_manager.add_order(order_id)
