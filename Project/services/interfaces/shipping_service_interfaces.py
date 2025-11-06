from typing import List, Optional, Dict, Any
from datetime import datetime
from domain.models import Order
from domain.enums import ShippingMethod, OrderStatus
from domain.value_objects import Money


class ShipmentManager:
    """Interface for shipment management"""
    def create_shipment(self, order_id: int, tracking_number: str) -> Dict[str, Any]:
        """Create a shipment for an order"""
        pass
    
    def get_shipment(self, shipment_id: int) -> Optional[Dict[str, Any]]:
        """Get a shipment by ID"""
        pass
    
    def get_shipment_by_order(self, order_id: int) -> Optional[Dict[str, Any]]:
        """Get a shipment by order ID"""
        pass
    
    def update_shipment_status(self, shipment_id: int, new_status: str) -> bool:
        """Update status of a shipment"""
        pass
    
    def cancel_shipment(self, shipment_id: int) -> bool:
        """Cancel a shipment"""
        pass
    
    def get_all_shipments(self) -> List[Dict[str, Any]]:
        """Get all shipments"""
        pass
    
    def get_shipments_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get shipments by status"""
        pass


class ShipmentTracker:
    """Interface for shipment tracking"""
    def track_shipment(self, tracking_number: str) -> Optional[Dict[str, Any]]:
        """Track a shipment by tracking number"""
        pass
    
    def generate_tracking_number(self, order_id: int) -> str:
        """Generate a tracking number for a shipment"""
        pass


class ShippingCalculator:
    """Interface for shipping calculations"""
    def calculate_shipping_cost(
        self, 
        order_items: List[Dict[str, Any]], 
        shipping_method: ShippingMethod,
        customer_discount_rate: float = 0.0,
        subtotal: Money = Money(0.0)
    ) -> Money:
        """Calculate shipping cost based on items, method, and customer discounts"""
        pass
    
    def get_delivery_estimate(self, shipping_method: ShippingMethod) -> tuple[int, int]:
        """Get estimated delivery days range for a shipping method"""
        pass


class OrderShipper:
    """Interface for order shipping operations"""
    def process_order_shipment(self, order: Order) -> Optional[Dict[str, Any]]:
        """Process shipping for an order"""
        pass