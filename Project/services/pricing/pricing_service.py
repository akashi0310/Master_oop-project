from typing import List, Optional, Tuple
from domain.models import Customer, OrderItem, Product, Promotion
from domain.value_objects import Money
from domain.enums import ShippingMethod
from services.pricing.strategies.membership_discount import MembershipDiscountStrategy
from services.pricing.strategies.promotional_discount import PromotionalDiscountStrategy
from services.pricing.strategies.bulk_discount import BulkDiscountStrategy
from services.pricing.strategies.loyalty_discount import LoyaltyDiscountStrategy


class PricingService:
    def __init__(self, promotion_repository=None):
        self.promotion_repository = promotion_repository
        self.membership_strategy = MembershipDiscountStrategy()
        self.promotional_strategy = PromotionalDiscountStrategy()
        self.bulk_strategy = BulkDiscountStrategy()
        self.loyalty_strategy = LoyaltyDiscountStrategy()
    
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
        """
        Calculate the total order price with all discounts and shipping
        Returns a dictionary with all pricing details
        """
        # Calculate subtotal
        subtotal = self._calculate_subtotal(order_items)
        
        # Apply membership discount
        membership_discount = self.membership_strategy.apply_discount(subtotal, customer)
        subtotal_after_membership = subtotal.subtract(membership_discount)
        
        # Apply promotional discount
        promo_discount = Money(0.0)
        applied_promotion = None
        if promo_code:
            promo_discount, applied_promotion = self.promotional_strategy.apply_discount(
                subtotal_after_membership, promo_code, promotions, order_items, products
            )
        subtotal_after_promo = subtotal_after_membership.subtract(promo_discount)
        
        # Apply bulk discount
        bulk_discount = self.bulk_strategy.apply_discount(subtotal_after_promo, order_items)
        subtotal_after_bulk = subtotal_after_promo.subtract(bulk_discount)
        
        # Apply loyalty discount
        loyalty_discount = Money(0.0)
        loyalty_points_used = 0
        if use_loyalty_points:
            loyalty_discount, loyalty_points_used = self.loyalty_strategy.apply_discount(
                subtotal_after_bulk, customer, use_all_points=False, points_to_use=loyalty_points_to_use
            )
        subtotal_after_loyalty = subtotal_after_bulk.subtract(loyalty_discount)
        
        # Calculate shipping
        total_weight = self._calculate_total_weight(order_items, products)
        shipping_cost = self._calculate_shipping(
            subtotal_after_loyalty, total_weight, shipping_method, customer
        )
        
        # Calculate tax
        tax = self._calculate_tax(subtotal_after_loyalty, customer)
        
        # Calculate total
        total = subtotal_after_loyalty.add(shipping_cost).add(tax)
        
        return {
            "subtotal": subtotal,
            "membership_discount": membership_discount,
            "subtotal_after_membership": subtotal_after_membership,
            "promo_discount": promo_discount,
            "applied_promotion": applied_promotion,
            "subtotal_after_promo": subtotal_after_promo,
            "bulk_discount": bulk_discount,
            "subtotal_after_bulk": subtotal_after_bulk,
            "loyalty_discount": loyalty_discount,
            "loyalty_points_used": loyalty_points_used,
            "subtotal_after_loyalty": subtotal_after_loyalty,
            "shipping_cost": shipping_cost,
            "tax": tax,
            "total": total,
            "total_weight": total_weight
        }
    
    def _calculate_subtotal(self, order_items: List[OrderItem]) -> Money:
        """Calculate the subtotal of all order items"""
        subtotal = Money(0.0)
        for item in order_items:
            item_total = item.unit_price.multiply(item.quantity)
            subtotal = subtotal.add(item_total)
        return subtotal
    
    def _calculate_total_weight(self, order_items: List[OrderItem], products: List[Product]) -> float:
        """Calculate the total weight of all order items"""
        product_lookup = {p.product_id: p for p in products}
        total_weight = 0.0
        
        for item in order_items:
            product = product_lookup.get(item.product_id)
            if product:
                total_weight += product.weight * item.quantity
        
        return total_weight
    
    def _calculate_shipping(
        self, 
        subtotal: Money, 
        total_weight: float, 
        shipping_method: ShippingMethod, 
        customer: Customer
    ) -> Money:
        """Calculate shipping cost based on method, weight, and customer membership"""
        base_cost = shipping_method.get_base_cost()
        weight_cost = total_weight * shipping_method.get_weight_multiplier()
        
        shipping_cost = Money(base_cost + weight_cost)
        
        # Apply membership shipping discount
        shipping_discount_rate = customer.get_shipping_discount_rate()
        if shipping_discount_rate > 0:
            shipping_cost = shipping_cost.multiply(1 - shipping_discount_rate)
        
        # Check for free shipping threshold
        free_threshold = shipping_method.get_free_shipping_threshold()
        if free_threshold > 0 and subtotal.amount >= free_threshold:
            shipping_cost = Money(0.0)
        
        return shipping_cost
    
    def _calculate_tax(self, subtotal: Money, customer: Customer) -> Money:
        """Calculate tax based on customer's address"""
        # Default tax rate
        tax_rate = 0.08
        
        # Adjust tax rate based on state (if address is available)
        if customer.address:
            if customer.address.contains_state("CA"):
                tax_rate = 0.0725
            elif customer.address.contains_state("NY"):
                tax_rate = 0.04
            elif customer.address.contains_state("TX"):
                tax_rate = 0.0625
        
        return subtotal.multiply(tax_rate)