from typing import List, Optional, Union, Protocol
from datetime import datetime
from ..value_objects.money import Money
from ..enums.order_status import OrderStatus
from ..interfaces.order_interfaces import (
    OrderInfo, 
    OrderStatusOperations, 
    OrderTrackingOperations, 
    OrderCalculationOperations
)
from .order_item import OrderItem


class OrderItemsProvider(Protocol):
    """Protocol for providing order items"""
    def get_items(self) -> List[OrderItem]:
        ...


class Order(
    OrderInfo,
    OrderStatusOperations,
    OrderTrackingOperations,
    OrderCalculationOperations
):
    """
    Order class that follows SOLID principles by delegating responsibilities
    to specialized components through composition.
    """
    
    def __init__(
        self,
        order_id: int,
        customer_id: int,
        items: List[OrderItem],
        status: Union[str, OrderStatus],
        created_at: datetime,
        total_price: Union[float, Money],
        shipping_cost: Union[float, Money],
        status_manager=None,
        tracking_manager=None,
        calculations_service=None
    ):
        # Validate basic order data
        if order_id <= 0:
            raise ValueError("Order ID must be positive")
        if customer_id <= 0:
            raise ValueError("Customer ID must be positive")
        if not items:
            raise ValueError("Order must have at least one item")
        if not isinstance(created_at, datetime):
            raise ValueError("Created at must be a datetime object")
        
        # Set basic order information
        self._order_id = order_id
        self._customer_id = customer_id
        self._items = items
        self._created_at = created_at
        self._total_price = Money(total_price) if isinstance(total_price, (float, int)) else total_price
        self._shipping_cost = Money(shipping_cost) if isinstance(shipping_cost, (float, int)) else shipping_cost
        
        # Initialize specialized managers (dependency injection)
        # Default implementations are created only if not provided
        if status_manager is None:
            from services.order_status_manager import OrderStatusManager
            self._status_manager = OrderStatusManager(OrderStatus(status.lower()))
        else:
            self._status_manager = status_manager
            
        if tracking_manager is None:
            from services.order_tracking_manager import OrderTrackingManager
            self._tracking_manager = OrderTrackingManager()
        else:
            self._tracking_manager = tracking_manager
            
        if calculations_service is None:
            from services.order_calculations_service import OrderCalculationsService
            
            # Create a wrapper for calculations service
            class OrderItemsProviderImpl:
                def __init__(self, items):
                    self._items = items
                
                def get_items(self):
                    return self._items
            
            self._calculations_service = OrderCalculationsService(OrderItemsProviderImpl(items))
        else:
            self._calculations_service = calculations_service
    
    # Properties for OrderInfo interface
    @property
    def order_id(self) -> int:
        """Get the order ID"""
        return self._order_id
    
    @property
    def customer_id(self) -> int:
        """Get the customer ID"""
        return self._customer_id
    
    @property
    def items(self) -> List[OrderItem]:
        """Get the order items"""
        return self._items
    
    @property
    def created_at(self) -> datetime:
        """Get the creation date"""
        return self._created_at
    
    @property
    def total_price(self) -> Money:
        """Get the total price"""
        return self._total_price
    
    @property
    def shipping_cost(self) -> Money:
        """Get the shipping cost"""
        return self._shipping_cost
    
    @property
    def status(self) -> OrderStatus:
        """Get the current order status"""
        return self._status_manager.status
    
    # Delegate status operations to OrderStatusManager
    def update_status(self, new_status: OrderStatus) -> None:
        """Update the order status"""
        self._status_manager.update_status(new_status)
    
    def can_be_cancelled(self) -> bool:
        """Check if the order can be cancelled"""
        return self._status_manager.can_be_cancelled()
    
    def cancel(self) -> None:
        """Cancel the order"""
        self._status_manager.cancel()
    
    def is_shipped(self) -> bool:
        """Check if the order has been shipped"""
        return self._status_manager.is_shipped()
    
    def is_delivered(self) -> bool:
        """Check if the order has been delivered"""
        return self._status_manager.is_delivered()
    
    def is_cancelled(self) -> bool:
        """Check if the order has been cancelled"""
        return self._status_manager.is_cancelled()
    
    # Delegate tracking operations to OrderTrackingManager
    @property
    def tracking_number(self) -> Optional[str]:
        """Get the tracking number"""
        return self._tracking_manager.tracking_number
    
    @tracking_number.setter
    def tracking_number(self, value: str) -> None:
        """Set the tracking number"""
        self._tracking_manager.add_tracking_number(value)
    
    @property
    def payment_method(self) -> Optional[str]:
        """Get the payment method"""
        return self._tracking_manager.payment_method
    
    def add_tracking_number(self, tracking_number: str) -> None:
        """Add a tracking number to the order"""
        self._tracking_manager.add_tracking_number(tracking_number)
    
    def set_payment_method(self, payment_method: str) -> None:
        """Set the payment method for the order"""
        self._tracking_manager.set_payment_method(payment_method)
    
    # Delegate calculation operations to OrderCalculationsService
    def get_subtotal(self) -> Money:
        """Calculate the subtotal of all items"""
        return self._calculations_service.get_subtotal()
    
    def get_total_weight(self) -> float:
        """Calculate the total weight of all items"""
        return self._calculations_service.get_total_weight()
    
    def get_days_since_creation(self) -> int:
        """Get the number of days since the order was created"""
        return (datetime.now() - self._created_at).days
