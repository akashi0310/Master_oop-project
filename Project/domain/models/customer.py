from typing import Optional, Union, Protocol, List
from ..value_objects.email import Email
from ..value_objects.address import Address
from ..enums.membership_tier import MembershipTier
from ..interfaces.customer_interfaces import (
    CustomerInfo,
    LoyaltyOperations,
    MembershipOperations,
    OrderHistoryOperations,
    CustomerValidator as CustomerValidatorABC,
)


# Protocols to invert dependencies away from services layer

class LoyaltyPointsCalculator(Protocol):
    def get_loyalty_points_multiplier(self) -> float:
        ...


class LoyaltyPointsManagerProtocol(Protocol):
    @property
    def points(self) -> int:
        ...
    @points.setter
    def points(self, value: int) -> None:
        ...
    def add_points(self, points: int, calculator: LoyaltyPointsCalculator) -> None:
        ...
    def redeem_points(self, points: int) -> bool:
        ...


class MembershipManagerProtocol(Protocol):
    @property
    def membership_tier(self) -> MembershipTier:
        ...
    def upgrade_membership(self, new_tier: MembershipTier) -> None:
        ...
    def get_discount_rate(self) -> float:
        ...
    def get_shipping_discount_rate(self) -> float:
        ...
    def can_place_orders(self) -> bool:
        ...
    def get_loyalty_points_multiplier(self) -> float:
        ...


class OrderHistoryManagerProtocol(Protocol):
    @property
    def order_history(self) -> List[int]:
        ...
    def add_order(self, order_id: int) -> None:
        ...


# Default domain-level implementations to avoid importing from services layer

class _DefaultCustomerValidator(CustomerValidatorABC):
    """Default implementation of customer validation (domain-local)"""
    def validate_customer_data(self, customer_id: int, name: str, loyalty_points: int) -> None:
        if not name or not name.strip():
            raise ValueError("Customer name cannot be empty")
        if customer_id <= 0:
            raise ValueError("Customer ID must be positive")
        if loyalty_points < 0:
            raise ValueError("Loyalty points cannot be negative")


class _DefaultMembershipManager(MembershipManagerProtocol):
    """Domain-local membership manager"""
    def __init__(self, membership_tier: MembershipTier):
        self._membership_tier = membership_tier

    @property
    def membership_tier(self) -> MembershipTier:
        return self._membership_tier

    def upgrade_membership(self, new_tier: MembershipTier) -> None:
        if new_tier == MembershipTier.SUSPENDED:
            raise ValueError("Cannot upgrade to suspended status")
        self._membership_tier = new_tier

    def get_discount_rate(self) -> float:
        return self._membership_tier.get_discount_rate()

    def get_shipping_discount_rate(self) -> float:
        return self._membership_tier.get_shipping_discount_rate()

    def can_place_orders(self) -> bool:
        return self._membership_tier.can_place_orders()

    def get_loyalty_points_multiplier(self) -> float:
        return self._membership_tier.get_loyalty_points_multiplier()


class _DefaultLoyaltyPointsManager(LoyaltyPointsManagerProtocol):
    """Domain-local loyalty points manager"""
    def __init__(self, initial_points: int = 0):
        if initial_points < 0:
            raise ValueError("Initial loyalty points cannot be negative")
        self._points = initial_points

    @property
    def points(self) -> int:
        return self._points

    @points.setter
    def points(self, value: int) -> None:
        if value < 0:
            raise ValueError("Loyalty points cannot be negative")
        self._points = value

    def add_points(self, points: int, calculator: LoyaltyPointsCalculator) -> None:
        if points <= 0:
            raise ValueError("Points to add must be positive")
        multiplier = calculator.get_loyalty_points_multiplier()
        self._points += int(points * multiplier)

    def redeem_points(self, points: int) -> bool:
        if points <= 0:
            raise ValueError("Points to redeem must be positive")
        if self._points >= points:
            self._points -= points
            return True
        return False


class _DefaultOrderHistoryManager(OrderHistoryManagerProtocol):
    """Domain-local order history manager"""
    def __init__(self):
        self._order_history: List[int] = []

    @property
    def order_history(self) -> List[int]:
        return self._order_history.copy()

    def add_order(self, order_id: int) -> None:
        if order_id <= 0:
            raise ValueError("Order ID must be positive")
        self._order_history.append(order_id)


class Customer(
    CustomerInfo,
    LoyaltyOperations,
    MembershipOperations,
    OrderHistoryOperations
):
    """
    Customer class that follows SOLID principles by delegating
    responsibilities to specialized components via dependency inversion.
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
        validator: Optional[CustomerValidatorABC] = None,
        membership_manager: Optional[MembershipManagerProtocol] = None,
        loyalty_manager: Optional[LoyaltyPointsManagerProtocol] = None,
        order_history_manager: Optional[OrderHistoryManagerProtocol] = None
    ):
        # Use dependency injection for validation
        self._validator = validator or _DefaultCustomerValidator()

        # Validate customer data
        self._validator.validate_customer_data(customer_id, name, loyalty_points)

        # Set basic customer information
        self.customer_id = customer_id
        self.name = name.strip()
        self.email = Email(email) if isinstance(email, str) else email
        self.phone = phone.strip() if phone else None
        self.address = Address.from_string(address) if isinstance(address, str) else address

        # Determine tier
        tier = MembershipTier(membership_tier.lower()) if isinstance(membership_tier, str) else membership_tier

        # Initialize specialized managers through DI with domain-local defaults
        self._membership_manager: MembershipManagerProtocol = membership_manager or _DefaultMembershipManager(tier)
        self._loyalty_manager: LoyaltyPointsManagerProtocol = loyalty_manager or _DefaultLoyaltyPointsManager(loyalty_points)
        self._order_history_manager: OrderHistoryManagerProtocol = order_history_manager or _DefaultOrderHistoryManager()

    # Properties to access managed data
    @property
    def membership_tier(self) -> MembershipTier:
        """Get current membership tier"""
        return self._membership_manager.membership_tier

    @property
    def loyalty_points(self) -> int:
        """Get current loyalty points"""
        return self._loyalty_manager.points

    @loyalty_points.setter
    def loyalty_points(self, value: int) -> None:
        """Set loyalty points"""
        self._loyalty_manager.points = value

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
