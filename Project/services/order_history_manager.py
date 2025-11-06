from typing import List


class OrderHistoryManager:
    """Manages order history for a customer"""
    
    def __init__(self):
        self._order_history: List[int] = []
    
    @property
    def order_history(self) -> List[int]:
        """Get a copy of the order history"""
        return self._order_history.copy()
    
    def add_order(self, order_id: int) -> None:
        """Add an order ID to the customer's order history"""
        if order_id <= 0:
            raise ValueError("Order ID must be positive")
        self._order_history.append(order_id)
    
    def get_order_count(self) -> int:
        """Get the total number of orders"""
        return len(self._order_history)