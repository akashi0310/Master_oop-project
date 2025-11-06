from datetime import datetime
from typing import Optional
from domain.enums.order_status import OrderStatus


class OrderStatusManager:
    """Manages order status transitions and validation"""
    
    def __init__(self, initial_status: OrderStatus):
        self._status = initial_status
        self.shipped_at: Optional[datetime] = None
        self.delivered_at: Optional[datetime] = None
    
    @property
    def status(self) -> OrderStatus:
        """Get current order status"""
        return self._status
    
    def update_status(self, new_status: OrderStatus) -> None:
        """Update the order status with validation"""
        if self._status.is_final_state():
            raise ValueError(f"Cannot change status from final state: {self._status.value}")
        
        self._status = new_status
        
        # Set timestamps for specific status changes
        if new_status == OrderStatus.SHIPPED:
            self.shipped_at = datetime.now()
        elif new_status == OrderStatus.DELIVERED:
            self.delivered_at = datetime.now()
    
    def can_be_cancelled(self) -> bool:
        """Check if the order can be cancelled"""
        return self._status.can_be_cancelled()
    
    def cancel(self) -> None:
        """Cancel the order"""
        if not self.can_be_cancelled():
            raise ValueError(f"Order cannot be cancelled in {self._status.value} status")
        self.update_status(OrderStatus.CANCELLED)
    
    def is_shipped(self) -> bool:
        """Check if the order has been shipped"""
        return self._status == OrderStatus.SHIPPED
    
    def is_delivered(self) -> bool:
        """Check if the order has been delivered"""
        return self._status == OrderStatus.DELIVERED
    
    def is_cancelled(self) -> bool:
        """Check if the order has been cancelled"""
        return self._status == OrderStatus.CANCELLED