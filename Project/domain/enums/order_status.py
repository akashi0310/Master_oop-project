from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    
    def can_be_cancelled(self) -> bool:
        """Check if order can be cancelled in current status"""
        return self in [OrderStatus.PENDING, OrderStatus.CONFIRMED, OrderStatus.PROCESSING]
    
    def can_be_shipped(self) -> bool:
        """Check if order can be shipped in current status"""
        return self in [OrderStatus.CONFIRMED, OrderStatus.PROCESSING]
    
    def is_final_state(self) -> bool:
        """Check if order is in a final state"""
        return self in [OrderStatus.DELIVERED, OrderStatus.CANCELLED, OrderStatus.REFUNDED]
    
    def is_active(self) -> bool:
        """Check if order is still active (not cancelled or refunded)"""
        return self not in [OrderStatus.CANCELLED, OrderStatus.REFUNDED]