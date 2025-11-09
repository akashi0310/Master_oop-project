import datetime
import random
from typing import Dict, List, Any

from ecommerce_order_management.domain.models.order import Order, OrderId
from ecommerce_order_management.domain.models.customer import Customer, CustomerId
from ecommerce_order_management.domain.models.product import Product, ProductId
from ecommerce_order_management.domain.models.order_item import OrderItem
from ecommerce_order_management.domain.value_objects.money import Money
from ecommerce_order_management.domain.enums.order_status import OrderStatus
from ecommerce_order_management.domain.enums.shipping_method import ShippingMethod
from ecommerce_order_management.domain.enums.membership_tier import MembershipTier

# Assuming these services are injected or globally accessible for simplicity in this refactor
# In a real application, these would be injected via dependency injection
from ecommerce_order_management.services.inventory_service import InventoryService
from ecommerce_order_management.services.pricing.pricing_service import PricingService
from ecommerce_order_management.services.pricing.strategies.membership_discount import MembershipDiscount
from ecommerce_order_management.services.pricing.strategies.promotional_discount import PromotionalDiscount
from ecommerce_order_management.services.pricing.strategies.bulk_discount import BulkDiscount
from ecommerce_order_management.services.pricing.strategies.loyalty_discount import LoyaltyDiscount

class OrderService:
    def __init__(self, orders: Dict[OrderId, Order], products: Dict[ProductId, Product], customers: Dict[CustomerId, Customer], inventory_service: InventoryService):
        self.orders = orders
        self.products = products
        self.customers = customers
        self.inventory_service = inventory_service
        self.next_order_id = 1 # This should ideally be managed by a persistent store
        self.pricing_service = PricingService([
            MembershipDiscount(),
            PromotionalDiscount(),
            BulkDiscount(),
            LoyaltyDiscount()
        ])

    def create_order(self, customer_id: CustomerId, order_items: List[OrderItem], shipping_method: ShippingMethod = ShippingMethod.STANDARD, promo_code: str = None) -> Order | None:
        customer = self.customers.get(customer_id)
        if not customer:
            return None

        # Validate customer membership is active
        if customer.membership_tier == MembershipTier.SUSPENDED:
            return None

        # Check all products available and deduct stock
        for item in order_items:
            product = self.products.get(item.product_id)
            if not product or product.quantity_available < item.quantity:
                return None
            # Stock deduction will happen after successful payment in a real system,
            # but for now, we'll deduct it here as per the original process_order.
            # This will be moved to a separate payment/inventory flow later.
            # self.inventory_service.deduct_stock(item.product_id, item.quantity, self.next_order_id)

        # Calculate subtotal and total weight
        subtotal_amount = sum(item.quantity * item.unit_price.amount for item in order_items)
        total_weight = sum(self.products[item.product_id].weight * item.quantity for item in order_items)

        # Create a temporary order object for pricing calculation
        temp_order = Order(
            order_id=self.next_order_id,
            customer_id=customer_id,
            items=order_items,
            status=OrderStatus.PENDING,
            created_at=datetime.datetime.now(),
            total_price=Money(subtotal_amount, "USD"),
            shipping_cost=Money(0.0, "USD"), # Will be calculated by shipping service
            promo_code=promo_code
        )

        # Calculate total price using pricing service
        final_price_money = self.pricing_service.calculate_total(temp_order, customer, self.products, {}) # Promotions will be passed here

        order_id = self.next_order_id
        self.next_order_id += 1
        order = Order(
            order_id=order_id,
            customer_id=customer_id,
            items=order_items,
            status=OrderStatus.PENDING,
            created_at=datetime.datetime.now(),
            total_price=final_price_money,
            shipping_cost=Money(0.0, "USD"), # Placeholder, will be set by shipping service
            promo_code=promo_code
        )
        self.orders[order_id] = order
        customer.order_history.append(order_id)
        customer.loyalty_points += int(subtotal_amount) # Award loyalty points based on subtotal

        return order

    def get_order(self, order_id: OrderId) -> Order | None:
        return self.orders.get(order_id)

    def update_order_status(self, order_id: OrderId, new_status: OrderStatus) -> Order | None:
        order = self.orders.get(order_id)
        if not order:
            return None
        order.status = new_status
        return order

    def apply_additional_discount(self, order_id: OrderId, discount_percent: float, reason: str) -> Order | None:
        order = self.orders.get(order_id)
        if not order:
            return None
        if order.status != OrderStatus.PENDING:
            return None
        order.total_price = Money(order.total_price.amount * (1 - discount_percent / 100), "USD")
        return order

    def cancel_order(self, order_id: OrderId, reason: str) -> bool:
        order = self.orders.get(order_id)
        if not order:
            return False

        if order.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
            return False

        for item in order.items:
            self.inventory_service.restore_stock(item.product_id, item.quantity, order_id)

        order.status = OrderStatus.CANCELLED
        return True