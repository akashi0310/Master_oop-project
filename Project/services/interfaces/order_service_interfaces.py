from typing import List, Optional, Dict, Any
from domain.models import Order, OrderItem, Customer, Product, Promotion
from domain.enums import OrderStatus
from domain.value_objects import Money


class OrderRepository:
    """Interface for order repository operations"""
    def add_order(self, order: Order) -> None:
        """Add a new order to the repository"""
        pass
    
    def get_order(self, order_id: int) -> Optional[Order]:
        """Get an order by ID"""
        pass
    
    def get_all_orders(self) -> List[Order]:
        """Get all orders"""
        pass
    
    def get_orders_by_customer(self, customer_id: int) -> List[Order]:
        """Get all orders for a specific customer"""
        pass
    
    def get_orders_by_status(self, status: OrderStatus) -> List[Order]:
        """Get all orders with a specific status"""
        pass
    
    def update_order(self, order: Order) -> bool:
        """Update an order in the repository"""
        pass
    
    def remove_order(self, order_id: int) -> bool:
        """Remove an order from the repository"""
        pass


class OrderValidator:
    """Interface for order validation"""
    def validate_order_items(self, order_items: List[OrderItem], products: List[Product]) -> bool:
        """Validate order items against available products"""
        pass
    
    def validate_customer(self, customer: Customer) -> bool:
        """Validate if customer can place orders"""
        pass
    
    def validate_payment(self, payment_info: Dict[str, Any], total: Money) -> bool:
        """Validate payment information"""
        pass


class OrderProcessor:
    """Interface for order processing operations"""
    def create_order(
        self,
        customer_id: int,
        order_items: List[OrderItem],
        payment_info: Dict[str, Any],
        products: List[Product],
        customer: Customer,
        promotions: List[Promotion],
        promo_code: Optional[str] = None,
        shipping_method: str = "standard",
        loyalty_points_to_use: int = 0
    ) -> Optional[Order]:
        """Create a new order with all validations and calculations"""
        pass
    
    def cancel_order(self, order_id: int, reason: str) -> bool:
        """Cancel an order and restore inventory"""
        pass
    
    def update_order_status(self, order_id: int, new_status: OrderStatus) -> bool:
        """Update status of an order"""
        pass


class OrderDiscountManager:
    """Interface for managing order discounts"""
    def apply_additional_discount(self, order_id: int, discount_percent: float, reason: str) -> bool:
        """Apply an additional discount to an order"""
        pass
    
    def calculate_discount(self, order: Order, discount_info: Dict[str, Any]) -> Money:
        """Calculate discount for an order"""
        pass