from typing import List, Optional
from datetime import datetime
from domain.models import Order
from repositories.interfaces.order_repository import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    """In-memory implementation of OrderRepository"""
    
    def __init__(self):
        self._orders: List[Order] = []
        self._next_order_id = 1
    
    def add(self, order: Order) -> None:
        """Add a new order to the repository"""
        if any(o.order_id == order.order_id for o in self._orders):
            raise ValueError(f"Order with ID {order.order_id} already exists")
        self._orders.append(order)
        # Update next_order_id if the new order's ID is >= current next_id
        if order.order_id >= self._next_order_id:
            self._next_order_id = order.order_id + 1
    
    def get_by_id(self, order_id: int) -> Optional[Order]:
        """Get an order by its ID"""
        for order in self._orders:
            if order.order_id == order_id:
                return order
        return None
    
    def get_all(self) -> List[Order]:
        """Get all orders in the repository"""
        return self._orders.copy()
    
    def update(self, order: Order) -> bool:
        """Update an existing order"""
        for i, existing_order in enumerate(self._orders):
            if existing_order.order_id == order.order_id:
                self._orders[i] = order
                return True
        return False
    
    def delete(self, order_id: int) -> bool:
        """Delete an order by its ID"""
        for i, order in enumerate(self._orders):
            if order.order_id == order_id:
                del self._orders[i]
                return True
        return False
    
    def get_by_customer(self, customer_id: int) -> List[Order]:
        """Get all orders for a specific customer"""
        return [o for o in self._orders if o.customer_id == customer_id]
    
    def get_by_status(self, status: str) -> List[Order]:
        """Get all orders with a specific status"""
        return [o for o in self._orders if o.status.value == status.lower()]
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Order]:
        """Get all orders within a date range"""
        return [
            o for o in self._orders 
            if start_date <= o.created_at <= end_date
        ]
    
    def get_pending_orders(self) -> List[Order]:
        """Get all pending orders"""
        return self.get_by_status("pending")
    
    def get_shipped_orders(self) -> List[Order]:
        """Get all shipped orders"""
        return self.get_by_status("shipped")
    
    def get_delivered_orders(self) -> List[Order]:
        """Get all delivered orders"""
        return self.get_by_status("delivered")
    
    def get_cancelled_orders(self) -> List[Order]:
        """Get all cancelled orders"""
        return self.get_by_status("cancelled")
    
    def get_next_order_id(self) -> int:
        """Get the next available order ID"""
        order_id = self._next_order_id
        self._next_order_id += 1
        return order_id