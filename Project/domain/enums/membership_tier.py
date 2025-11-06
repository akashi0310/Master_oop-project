from enum import Enum


class MembershipTier(Enum):
    STANDARD = "standard"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    SUSPENDED = "suspended"
    
    def get_discount_rate(self) -> float:
        """Get discount rate for this membership tier"""
        discount_rates = {
            MembershipTier.STANDARD: 0.0,
            MembershipTier.BRONZE: 0.03,
            MembershipTier.SILVER: 0.07,
            MembershipTier.GOLD: 0.15,
            MembershipTier.SUSPENDED: 0.0
        }
        return discount_rates[self]
    
    def get_shipping_discount_rate(self) -> float:
        """Get shipping discount rate for this membership tier"""
        shipping_discounts = {
            MembershipTier.STANDARD: 0.0,
            MembershipTier.BRONZE: 0.0,
            MembershipTier.SILVER: 0.0,
            MembershipTier.GOLD: 0.5,  # Gold members get 50% off shipping
            MembershipTier.SUSPENDED: 0.0
        }
        return shipping_discounts[self]
    
    def can_place_orders(self) -> bool:
        """Check if customer can place orders with this membership tier"""
        return self != MembershipTier.SUSPENDED
    
    def get_loyalty_points_multiplier(self) -> float:
        """Get loyalty points earning multiplier for this tier"""
        multipliers = {
            MembershipTier.STANDARD: 1.0,
            MembershipTier.BRONZE: 1.2,
            MembershipTier.SILVER: 1.5,
            MembershipTier.GOLD: 2.0,
            MembershipTier.SUSPENDED: 0.0
        }
        return multipliers[self]