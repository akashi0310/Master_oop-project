from typing import List, Optional
from domain.models import Order
from datetime import datetime


class OrderRepository:
    """Repository interface for Order entities"""
    
    def add(self, order: Order) -> None:
        """Add a new order to the repository"""
        raise NotImplementedError
    
    def get_by_id(self, order_id: int) -> Optional[Order]:
        """Get an order by its ID"""
        raise NotImplementedError
    
    def get_all(self) -> List[Order]:
        """Get all orders in the repository"""
        raise NotImplementedError
    
    def update(self, order: Order) -> bool:
        """Update an existing order"""
        raise NotImplementedError
    
    def delete(self, order_id: int) -> bool:
        """Delete an order by its ID"""
        raise NotImplementedError
    
    def get_by_customer(self, customer_id: int) -> List[Order]:
        """Get all orders for a specific customer"""
        raise NotImplementedError
    
    def get_by_status(self, status: str) -> List[Order]:
        """Get all orders with a specific status"""
        raise NotImplementedError
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Order]:
        """Get all orders within a date range"""
        raise NotImplementedError
    
    def get_pending_orders(self) -> List[Order]:
        """Get all pending orders"""
        raise NotImplementedError
    
    def get_shipped_orders(self) -> List[Order]:
        """Get all shipped orders"""
        raise NotImplementedError
    
    def get_delivered_orders(self) -> List[Order]:
        """Get all delivered orders"""
        raise NotImplementedError
    
    def get_cancelled_orders(self) -> List[Order]:
        """Get all cancelled orders"""
        raise NotImplementedError