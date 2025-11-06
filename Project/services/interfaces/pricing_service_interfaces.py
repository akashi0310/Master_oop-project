from typing import List, Optional, Dict, Any
from domain.models import Customer, OrderItem, Product, Promotion
from domain.value_objects import Money
from domain.enums import ShippingMethod


class PricingCalculator:
    """Interface for pricing calculations"""
    def calculate_order_total(
        self,
        order_items: List[OrderItem],
        customer: Customer,
        products: List[Product],
        promotions: List[Promotion],
        promo_code: Optional[str] = None,
        shipping_method: ShippingMethod = ShippingMethod.STANDARD,
        use_loyalty_points: bool = False,
        loyalty_points_to_use: int = 0
    ) -> dict:
        """Calculate total order price with all discounts and shipping"""
        pass
    
    def calculate_subtotal(self, order_items: List[OrderItem]) -> Money:
        """Calculate the subtotal of all order items"""
        pass
    
    def calculate_shipping(
        self, 
        subtotal: Money, 
        total_weight: float, 
        shipping_method: ShippingMethod, 
        customer: Customer
    ) -> Money:
        """Calculate shipping cost based on method, weight, and customer membership"""
        pass
    
    def calculate_tax(self, subtotal: Money, customer: Customer) -> Money:
        """Calculate tax based on customer's address"""
        pass


class DiscountStrategy:
    """Interface for discount strategies"""
    def apply_discount(
        self, 
        subtotal: Money, 
        customer: Customer, 
        promo_code: Optional[str] = None,
        promotions: List[Promotion] = None,
        order_items: List[OrderItem] = None,
        use_all_points: bool = False,
        points_to_use: int = 0
    ) -> tuple[Money, Optional[Promotion]]:
        """Apply discount and return (discount_amount, applied_promotion)"""
        pass


class ShippingCalculator:
    """Interface for shipping calculations"""
    def calculate_shipping_cost(
        self, 
        order_items: List[Dict[str, Any]], 
        shipping_method: ShippingMethod,
        customer_discount_rate: float = 0.0,
        subtotal: Money = Money(0.0)
    ) -> Money:
        """Calculate shipping cost based on items, method, and customer discounts"""
        pass
    
    def get_delivery_estimate(self, shipping_method: ShippingMethod) -> tuple[int, int]:
        """Get estimated delivery days range for a shipping method"""
        pass