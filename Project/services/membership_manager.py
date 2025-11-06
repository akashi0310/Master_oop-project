from abc import ABC, abstractmethod
from typing import Protocol
from domain.enums.membership_tier import MembershipTier


class MembershipValidator(Protocol):
    """Protocol for validating membership operations"""
    def can_place_orders(self) -> bool:
        ...


class MembershipManager:
    """Manages membership tier operations for a customer"""
    
    def __init__(self, membership_tier: MembershipTier):
        self._membership_tier = membership_tier
    
    @property
    def membership_tier(self) -> MembershipTier:
        """Get current membership tier"""
        return self._membership_tier
    
    def upgrade_membership(self, new_tier: MembershipTier) -> None:
        """Upgrade the customer's membership tier"""
        if new_tier == MembershipTier.SUSPENDED:
            raise ValueError("Cannot upgrade to suspended status")
        self._membership_tier = new_tier
    
    def get_discount_rate(self) -> float:
        """Get the discount rate for this customer's membership tier"""
        return self._membership_tier.get_discount_rate()
    
    def get_shipping_discount_rate(self) -> float:
        """Get the shipping discount rate for this customer's membership tier"""
        return self._membership_tier.get_shipping_discount_rate()
    
    def can_place_orders(self) -> bool:
        """Check if customer can place orders with current membership tier"""
        return self._membership_tier.can_place_orders()
    
    def get_loyalty_points_multiplier(self) -> float:
        """Get loyalty points earning multiplier for current tier"""
        return self._membership_tier.get_loyalty_points_multiplier()