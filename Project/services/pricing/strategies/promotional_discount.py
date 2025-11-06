from typing import List, Optional
from domain.models import Promotion, OrderItem, Product
from domain.value_objects import Money


class PromotionalDiscountStrategy:
    def apply_discount(self, subtotal: Money, promo_code: str, promotions: List[Promotion], 
                    order_items: List[OrderItem], products: List[Product]) -> tuple[Money, Optional[Promotion]]:
        """Apply promotional discount if valid"""
        # Find the promotion by code
        promotion = None
        for promo in promotions:
            if promo.code == promo_code.upper():
                promotion = promo
                break
        
        if not promotion:
            return Money(0.0), None
        
        # Check if promotion is valid
        if not promotion.is_valid():
            return Money(0.0), None
        
        # Check if minimum purchase is met
        if not promotion.meets_minimum_purchase(subtotal):
            return Money(0.0), None
        
        # Check if any items match the promotion category
        if not self._has_applicable_items(promotion, order_items, products):
            return Money(0.0), None
        
        # Calculate and apply discount
        discount_amount = promotion.calculate_discount(subtotal)
        return discount_amount, promotion
    
    def _has_applicable_items(self, promotion: Promotion, order_items: List[OrderItem], 
                            products: List[Product]) -> bool:
        """Check if any order items match the promotion category"""
        if promotion.category == "all":
            return True
        
        # Create a product lookup dictionary
        product_lookup = {p.product_id: p for p in products}
        
        for item in order_items:
            product = product_lookup.get(item.product_id)
            if product and promotion.is_applicable_to_category(product.category):
                return True
        
        return False