from typing import List, Optional, Protocol
from datetime import datetime
from domain.value_objects.money import Money
from domain.enums.order_status import OrderStatus
from domain.models.order_item import OrderItem


class OrderInfo(Protocol):
    """Protocol for basic order information"""
    @property
    def order_id(self) -> int: ...
    
    @property
    def customer_id(self) -> int: ...
    
    @property
    def items(self) -> List[OrderItem]: ...
    
    @property
    def created_at(self) -> datetime: ...
    
    @property
    def total_price(self) -> Money: ...
    
    @property
    def shipping_cost(self) -> Money: ...


    def get_days_since_creation(self) -> int: ...


class OrderStatusOperations(Protocol):
    """Protocol for order status operations"""
    def update_status(self, new_status: OrderStatus) -> None: ...
    
    def can_be_cancelled(self) -> bool: ...
    
    def cancel(self) -> None: ...
    
    def is_shipped(self) -> bool: ...
    
    def is_delivered(self) -> bool: ...
    
    def is_cancelled(self) -> bool: ...


class OrderTrackingOperations(Protocol):
    """Protocol for order tracking operations"""
    @property
    def tracking_number(self) -> Optional[str]: ...
    
    @property
    def payment_method(self) -> Optional[str]: ...
    
    def add_tracking_number(self, tracking_number: str) -> None: ...
    
    def set_payment_method(self, payment_method: str) -> None: ...


class OrderCalculationOperations(Protocol):
    """Protocol for order calculation operations"""
    def get_subtotal(self) -> Money: ...
    
    def get_total_weight(self) -> float: ...