import datetime
import random
from typing import Dict, Any, List

from ecommerce_order_management.domain.models.order import Order, OrderId
from ecommerce_order_management.domain.models.customer import Customer
from ecommerce_order_management.domain.models.product import Product, ProductId
from ecommerce_order_management.domain.value_objects.money import Money
from ecommerce_order_management.domain.enums.membership_tier import MembershipTier
from ecommerce_order_management.domain.enums.shipping_method import ShippingMethod

class ShippingService:
    def __init__(self, shipments: Dict[int, Dict[str, Any]], products: Dict[ProductId, Product]):
        self.shipments = shipments
        self.products = products
        self.next_shipment_id = 1 # This should ideally be managed by a persistent store

    def calculate_shipping_cost(self, order: Order, customer: Customer, shipping_method: ShippingMethod) -> Money:
        total_weight = sum(self.products[item.product_id].weight * item.quantity for item in order.items)
        shipping_cost_amount = 0.0

        if shipping_method == ShippingMethod.EXPRESS:
            shipping_cost_amount = 25 + (total_weight * 0.5)
            if customer.membership_tier == MembershipTier.GOLD:
                shipping_cost_amount *= 0.5
        elif shipping_method == ShippingMethod.STANDARD:
            if order.total_price.amount < 50:
                shipping_cost_amount = 5 + (total_weight * 0.2)
            else:
                shipping_cost_amount = 0.0  # Free shipping over $50
        elif shipping_method == ShippingMethod.OVERNIGHT:
            shipping_cost_amount = 50 + (total_weight * 1.0)
        
        return Money(shipping_cost_amount, "USD")

    def create_shipment(self, order_id: OrderId) -> Dict[str, Any]:
        shipment_id = self.next_shipment_id
        self.next_shipment_id += 1
        tracking_number = f"TRACK{order_id}{random.randint(1000, 9999)}"
        shipment = {
            'shipment_id': shipment_id,
            'order_id': order_id,
            'tracking_number': tracking_number,
            'created_at': datetime.datetime.now(),
            'status': 'in_transit'
        }
        self.shipments[shipment_id] = shipment
        return shipment