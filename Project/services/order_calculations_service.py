from typing import List, Protocol
from domain.value_objects.money import Money
from domain.models.order_item import OrderItem


class OrderItemsProvider(Protocol):
    """Protocol for providing order items"""
    def get_items(self) -> List[OrderItem]:
        ...


class OrderCalculationsService:
    """Handles order-related calculations"""
    
    def __init__(self, items_provider: OrderItemsProvider):
        self._items_provider = items_provider
    
    def get_subtotal(self) -> Money:
        """Calculate the subtotal of all items"""
        subtotal = Money(0.0)
        items = self._items_provider.get_items()
        
        for item in items:
            item_total = item.unit_price.multiply(item.quantity)
            subtotal = subtotal.add(item_total)
        return subtotal
    
    def get_total_weight(self) -> float:
        """Calculate the total weight of all items"""
        total_weight = 0.0
        items = self._items_provider.get_items()
        
        for item in items:
            # Weight is stored in OrderItem
            total_weight += getattr(item, 'weight', 0.0) * item.quantity
        return total_weight