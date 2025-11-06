from typing import List, Optional, Dict, Any
from datetime import datetime
from domain.models import Order
from domain.enums import ShippingMethod, OrderStatus
from domain.value_objects import Money


class ShippingService:
    def __init__(self):
        self.shipments: List[Dict[str, Any]] = []
        self.next_shipment_id = 1
    
    def create_shipment(self, order_id: int, tracking_number: str) -> Dict[str, Any]:
        """Create a shipment for an order"""
        shipment = {
            'shipment_id': self.next_shipment_id,
            'order_id': order_id,
            'tracking_number': tracking_number,
            'created_at': datetime.now(),
            'status': 'in_transit',
            'estimated_delivery': None
        }
        
        self.shipments.append(shipment)
        self.next_shipment_id += 1
        
        return shipment
    
    def get_shipment(self, shipment_id: int) -> Optional[Dict[str, Any]]:
        """Get a shipment by ID"""
        for shipment in self.shipments:
            if shipment['shipment_id'] == shipment_id:
                return shipment
        return None
    
    def get_shipment_by_order(self, order_id: int) -> Optional[Dict[str, Any]]:
        """Get a shipment by order ID"""
        for shipment in self.shipments:
            if shipment['order_id'] == order_id:
                return shipment
        return None
    
    def update_shipment_status(self, shipment_id: int, new_status: str) -> bool:
        """Update the status of a shipment"""
        shipment = self.get_shipment(shipment_id)
        if shipment:
            shipment['status'] = new_status
            shipment['status_updated_at'] = datetime.now()
            
            # If delivered, set delivery time
            if new_status == 'delivered':
                shipment['delivered_at'] = datetime.now()
            
            return True
        return False
    
    def calculate_shipping_cost(
        self, 
        order_items: List[Dict[str, Any]], 
        shipping_method: ShippingMethod,
        customer_discount_rate: float = 0.0,
        subtotal: Money = Money(0.0)
    ) -> Money:
        """
        Calculate shipping cost based on items, method, and customer discounts
        """
        # Calculate total weight
        total_weight = sum(item.get('weight', 0) * item.get('quantity', 0) for item in order_items)
        
        # Calculate base shipping cost
        base_cost = shipping_method.get_base_cost()
        weight_cost = total_weight * shipping_method.get_weight_multiplier()
        
        shipping_cost = Money(base_cost + weight_cost)
        
        # Apply customer discount if applicable
        if customer_discount_rate > 0:
            shipping_cost = shipping_cost.multiply(1 - customer_discount_rate)
        
        # Check for free shipping threshold
        free_threshold = shipping_method.get_free_shipping_threshold()
        if free_threshold > 0 and subtotal.amount >= free_threshold:
            shipping_cost = Money(0.0)
        
        return shipping_cost
    
    def generate_tracking_number(self, order_id: int) -> str:
        """Generate a tracking number for a shipment"""
        import random
        return f"TRACK{order_id}{random.randint(1000, 9999)}"
    
    def get_delivery_estimate(self, shipping_method: ShippingMethod) -> tuple[int, int]:
        """Get estimated delivery days range for a shipping method"""
        return shipping_method.get_delivery_days()
    
    def get_all_shipments(self) -> List[Dict[str, Any]]:
        """Get all shipments"""
        return self.shipments.copy()
    
    def get_shipments_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get shipments by status"""
        return [s for s in self.shipments if s['status'] == status]
    
    def track_shipment(self, tracking_number: str) -> Optional[Dict[str, Any]]:
        """Track a shipment by tracking number"""
        for shipment in self.shipments:
            if shipment['tracking_number'] == tracking_number:
                return shipment
        return None
    
    def cancel_shipment(self, shipment_id: int) -> bool:
        """Cancel a shipment"""
        shipment = self.get_shipment(shipment_id)
        if shipment and shipment['status'] == 'in_transit':
            shipment['status'] = 'cancelled'
            shipment['cancelled_at'] = datetime.now()
            return True
        return False
    
    def process_order_shipment(self, order: Order) -> Optional[Dict[str, Any]]:
        """Process shipping for an order"""
        if order.status != OrderStatus.CONFIRMED:
            return None
        
        # Generate tracking number
        tracking_number = self.generate_tracking_number(order.order_id)
        
        # Create shipment
        shipment = self.create_shipment(order.order_id, tracking_number)
        
        # Update order with tracking number
        order.add_tracking_number(tracking_number)
        
        # Update order status
        order.update_status(OrderStatus.SHIPPED)
        
        return shipment
