from typing import List
from domain.models import OrderItem
from domain.value_objects import Money


class BulkDiscountStrategy:
    def __init__(self):
        # Define bulk discount tiers
        self.discount_tiers = [
            {"min_items": 10, "discount_rate": 0.05},  # 5% off for 10+ items
            {"min_items": 5, "discount_rate": 0.02}    # 2% off for 5+ items
        ]
    
    def apply_discount(self, subtotal: Money, order_items: List[OrderItem]) -> Money:
        """Apply bulk discount based on total quantity"""
        total_items = sum(item.quantity for item in order_items)
        
        # Find the applicable discount rate
        discount_rate = 0.0
        for tier in self.discount_tiers:
            if total_items >= tier["min_items"]:
                discount_rate = tier["discount_rate"]
        
        if discount_rate > 0:
            return subtotal.multiply(discount_rate)
        
        return Money(0.0)
    
    def get_applicable_discount_rate(self, total_items: int) -> float:
        """Get the discount rate for a given total quantity"""
        discount_rate = 0.0
        for tier in self.discount_tiers:
            if total_items >= tier["min_items"]:
                discount_rate = tier["discount_rate"]
        return discount_rate
    
    def get_next_discount_tier(self, total_items: int) -> dict:
        """Get the next discount tier the customer could reach"""
        for tier in sorted(self.discount_tiers, key=lambda x: x["min_items"], reverse=True):
            if total_items < tier["min_items"]:
                return tier
        return None