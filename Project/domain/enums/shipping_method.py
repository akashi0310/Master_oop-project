from enum import Enum


class ShippingMethod(Enum):
    STANDARD = "standard"
    EXPRESS = "express"
    OVERNIGHT = "overnight"
    
    def get_base_cost(self) -> float:
        """Get base cost for this shipping method"""
        base_costs = {
            ShippingMethod.STANDARD: 5.0,
            ShippingMethod.EXPRESS: 25.0,
            ShippingMethod.OVERNIGHT: 50.0
        }
        return base_costs[self]
    
    def get_weight_multiplier(self) -> float:
        """Get weight multiplier for this shipping method"""
        weight_multipliers = {
            ShippingMethod.STANDARD: 0.2,
            ShippingMethod.EXPRESS: 0.5,
            ShippingMethod.OVERNIGHT: 1.0
        }
        return weight_multipliers[self]
    
    def get_free_shipping_threshold(self) -> float:
        """Get minimum order amount for free shipping"""
        free_thresholds = {
            ShippingMethod.STANDARD: 50.0,  # Free shipping over $50
            ShippingMethod.EXPRESS: 0.0,   # No free shipping for express
            ShippingMethod.OVERNIGHT: 0.0  # No free shipping for overnight
        }
        return free_thresholds[self]
    
    def get_delivery_days(self) -> tuple[int, int]:
        """Get estimated delivery days range (min, max)"""
        delivery_days = {
            ShippingMethod.STANDARD: (5, 7),
            ShippingMethod.EXPRESS: (2, 3),
            ShippingMethod.OVERNIGHT: (1, 1)
        }
        return delivery_days[self]