from typing import List, Optional, Union
from datetime import datetime
from ..value_objects.money import Money
from ..enums.order_status import OrderStatus
from .order_item import OrderItem


class Order:
    def __init__(
        self,
        order_id: int,
        customer_id: int,
        items: List[OrderItem],
        status: str,
        created_at: datetime,
        total_price: Union[float, Money],
        shipping_cost: Union[float, Money]
    ):
        if order_id <= 0:
            raise ValueError("Order ID must be positive")
        if customer_id <= 0:
            raise ValueError("Customer ID must be positive")
        if not items:
            raise ValueError("Order must have at least one item")
        if not isinstance(created_at, datetime):
            raise ValueError("Created at must be a datetime object")
        
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
        self.status = OrderStatus(status.lower())
        self.created_at = created_at
        self.total_price = Money(total_price) if isinstance(total_price, (float, int)) else total_price
        self.shipping_cost = Money(shipping_cost) if isinstance(shipping_cost, (float, int)) else shipping_cost
        self.tracking_number: Optional[str] = None
        self.payment_method: Optional[str] = None
        self.shipped_at: Optional[datetime] = None
        self.delivered_at: Optional[datetime] = None
    
    def update_status(self, new_status: OrderStatus) -> None:
        """Update the order status"""
        if self.status.is_final_state():
            raise ValueError(f"Cannot change status from final state: {self.status.value}")
        
        self.status = new_status
        
        # Set timestamps for specific status changes
        if new_status == OrderStatus.SHIPPED:
            self.shipped_at = datetime.now()
        elif new_status == OrderStatus.DELIVERED:
            self.delivered_at = datetime.now()
    
    def can_be_cancelled(self) -> bool:
        """Check if the order can be cancelled"""
        return self.status.can_be_cancelled()
    
    def cancel(self) -> None:
        """Cancel the order"""
        if not self.can_be_cancelled():
            raise ValueError(f"Order cannot be cancelled in {self.status.value} status")
        self.update_status(OrderStatus.CANCELLED)
    
    def add_tracking_number(self, tracking_number: str) -> None:
        """Add tracking number to the order"""
        if not tracking_number or not tracking_number.strip():
            raise ValueError("Tracking number cannot be empty")
        self.tracking_number = tracking_number.strip()
    
    def set_payment_method(self, payment_method: str) -> None:
        """Set the payment method for the order"""
        if not payment_method or not payment_method.strip():
            raise ValueError("Payment method cannot be empty")
        self.payment_method = payment_method.strip()
    
    def get_subtotal(self) -> Money:
        """Calculate the subtotal of all items"""
        subtotal = Money(0.0)
        for item in self.items:
            item_total = item.unit_price.multiply(item.quantity)
            subtotal = subtotal.add(item_total)
        return subtotal
    
    def get_total_weight(self) -> float:
        """Calculate the total weight of all items"""
        # Note: This would need product information, which is not available in the Order model
        # This is a limitation that should be addressed in the service layer
        total_weight = 0.0
        for item in self.items:
            # Assuming weight is stored in OrderItem or accessible via product service
            total_weight += getattr(item, 'weight', 0.0) * item.quantity
        return total_weight
    
    def is_shipped(self) -> bool:
        """Check if the order has been shipped"""
        return self.status == OrderStatus.SHIPPED
    
    def is_delivered(self) -> bool:
        """Check if the order has been delivered"""
        return self.status == OrderStatus.DELIVERED
    
    def is_cancelled(self) -> bool:
        """Check if the order has been cancelled"""
        return self.status == OrderStatus.CANCELLED
    
    def get_days_since_creation(self) -> int:
        """Get the number of days since the order was created"""
        return (datetime.now() - self.created_at).days
