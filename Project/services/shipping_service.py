import datetime
from typing import Dict, Any, Optional, List
from domain.models import Order
from domain.enums import ShippingMethod
from domain.value_objects import Address, Money
from services.interfaces.shipping_service_interfaces import (
    ShipmentManager, 
    ShipmentTracker, 
    ShippingCalculator, 
    OrderShipper
)


class DefaultShipmentManager(ShipmentManager):
    """Default implementation of shipment management"""
    def __init__(self):
        self.shipments: Dict[str, Dict[str, Any]] = {}
    
    def create_shipment(self, order_id: int, shipping_method: ShippingMethod, tracking_number: str = None) -> str:
        """Create a new shipment for an order"""
        if order_id <= 0:
            raise ValueError("Order ID must be positive")
        
        if not tracking_number:
            tracking_number = self._generate_tracking_number()
        
        shipment_id = f"SHIP-{order_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        self.shipments[shipment_id] = {
            "shipment_id": shipment_id,
            "order_id": order_id,
            "shipping_method": shipping_method,
            "tracking_number": tracking_number,
            "status": "created",
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "events": []
        }
        
        return shipment_id
    
    def update_shipment_status(self, shipment_id: str, status: str, location: str = None, notes: str = None) -> bool:
        """Update the status of a shipment"""
        if not shipment_id or not shipment_id.strip():
            raise ValueError("Shipment ID is required")
        
        if not status or not status.strip():
            raise ValueError("Status is required")
        
        if shipment_id not in self.shipments:
            return False
        
        self.shipments[shipment_id]["status"] = status
        self.shipments[shipment_id]["updated_at"] = datetime.datetime.now()
        
        # Add tracking event
        event = {
            "timestamp": datetime.datetime.now(),
            "status": status,
            "location": location,
            "notes": notes
        }
        self.shipments[shipment_id]["events"].append(event)
        
        return True
    
    def get_shipment(self, shipment_id: str) -> Optional[Dict[str, Any]]:
        """Get shipment details by ID"""
        if not shipment_id or not shipment_id.strip():
            raise ValueError("Shipment ID is required")
        
        return self.shipments.get(shipment_id)
    
    def get_shipments_by_order(self, order_id: int) -> List[Dict[str, Any]]:
        """Get all shipments for an order"""
        if order_id <= 0:
            raise ValueError("Order ID must be positive")
        
        return [
            shipment for shipment in self.shipments.values()
            if shipment["order_id"] == order_id
        ]
    
    def _generate_tracking_number(self) -> str:
        """Generate a unique tracking number"""
        import uuid
        return str(uuid.uuid4()).replace("-", "").upper()[:16]


class DefaultShipmentTracker(ShipmentTracker):
    """Default implementation of shipment tracking"""
    def __init__(self, shipment_manager: ShipmentManager):
        self.shipment_manager = shipment_manager
    
    def track_shipment(self, tracking_number: str) -> Optional[Dict[str, Any]]:
        """Track a shipment by tracking number"""
        if not tracking_number or not tracking_number.strip():
            raise ValueError("Tracking number is required")
        
        # Find shipment by tracking number
        for shipment in self.shipment_manager.shipments.values():
            if shipment.get("tracking_number") == tracking_number:
                return {
                    "tracking_number": tracking_number,
                    "status": shipment["status"],
                    "events": shipment["events"],
                    "estimated_delivery": self._calculate_estimated_delivery(shipment)
                }
        
        return None
    
    def get_tracking_history(self, tracking_number: str) -> List[Dict[str, Any]]:
        """Get the tracking history for a shipment"""
        if not tracking_number or not tracking_number.strip():
            raise ValueError("Tracking number is required")
        
        shipment_info = self.track_shipment(tracking_number)
        if shipment_info:
            return shipment_info["events"]
        
        return []
    
    def _calculate_estimated_delivery(self, shipment: Dict[str, Any]) -> Optional[datetime.datetime]:
        """Calculate estimated delivery date based on shipping method and creation date"""
        shipping_method = shipment["shipping_method"]
        created_at = shipment["created_at"]
        
        if shipping_method == ShippingMethod.STANDARD:
            delivery_days = 5
        elif shipping_method == ShippingMethod.EXPRESS:
            delivery_days = 2
        elif shipping_method == ShippingMethod.OVERNIGHT:
            delivery_days = 1
        else:
            delivery_days = 7  # Default for unknown shipping methods
        
        return created_at + datetime.timedelta(days=delivery_days)


class DefaultShippingCalculator(ShippingCalculator):
    """Default implementation of shipping cost calculation"""
    def calculate_shipping_cost(self, order: Order, shipping_method: ShippingMethod, address: Address) -> Money:
        """Calculate shipping cost based on order, shipping method, and address"""
        if not order:
            raise ValueError("Order is required")
        
        if not address:
            raise ValueError("Address is required")
        
        # Base cost by shipping method
        if shipping_method == ShippingMethod.STANDARD:
            base_cost = 5.99
        elif shipping_method == ShippingMethod.EXPRESS:
            base_cost = 12.99
        elif shipping_method == ShippingMethod.OVERNIGHT:
            base_cost = 24.99
        else:
            base_cost = 7.99  # Default for unknown shipping methods
        
        # Additional cost based on order weight or size
        additional_cost = self._calculate_additional_cost(order)
        
        # Additional cost based on distance (simplified)
        distance_cost = self._calculate_distance_cost(address)
        
        total_cost = base_cost + additional_cost + distance_cost
        return Money(total_cost)
    
    def _calculate_additional_cost(self, order: Order) -> float:
        """Calculate additional cost based on order characteristics"""
        # In a real implementation, this would consider weight, dimensions, etc.
        # For now, we'll use a simple calculation based on item count
        item_count = len(order.items)
        return max(0, (item_count - 3) * 1.50)  # $1.50 for each item beyond the first 3
    
    def _calculate_distance_cost(self, address: Address) -> float:
        """Calculate additional cost based on shipping distance"""
        # In a real implementation, this would use distance calculation APIs
        # For now, we'll use a simple calculation based on region
        country = address.country.lower() if address.country else ""
        
        if country == "us" or country == "usa" or country == "united states":
            return 0.0  # No additional cost for domestic shipping
        elif country in ["ca", "can", "canada"]:
            return 5.0  # $5 for Canada
        elif country in ["mx", "mex", "mexico"]:
            return 10.0  # $10 for Mexico
        else:
            return 15.0  # $15 for international shipping


class DefaultOrderShipper(OrderShipper):
    """Default implementation of order shipping"""
    def __init__(self, shipment_manager: ShipmentManager, shipping_calculator: ShippingCalculator):
        self.shipment_manager = shipment_manager
        self.shipping_calculator = shipping_calculator
    
    def ship_order(self, order: Order, shipping_method: ShippingMethod, address: Address) -> Dict[str, Any]:
        """Ship an order and return shipment details"""
        if not order:
            raise ValueError("Order is required")
        
        if not address:
            raise ValueError("Address is required")
        
        # Calculate shipping cost
        shipping_cost = self.shipping_calculator.calculate_shipping_cost(order, shipping_method, address)
        
        # Create shipment
        shipment_id = self.shipment_manager.create_shipment(order.order_id, shipping_method)
        
        # Update order status
        order.status = "shipped"
        
        return {
            "shipment_id": shipment_id,
            "shipping_cost": shipping_cost,
            "shipping_method": shipping_method,
            "tracking_number": self.shipment_manager.get_shipment(shipment_id)["tracking_number"]
        }
    
    def get_shipping_cost_estimate(self, order: Order, shipping_method: ShippingMethod, address: Address) -> Money:
        """Get an estimate of shipping cost without creating a shipment"""
        if not order:
            raise ValueError("Order is required")
        
        if not address:
            raise ValueError("Address is required")
        
        return self.shipping_calculator.calculate_shipping_cost(order, shipping_method, address)


class ShippingService:
    """
    Refactored ShippingService that follows SOLID principles by delegating
    responsibilities to appropriate components.
    """
    
    def __init__(
        self,
        shipment_manager: Optional[ShipmentManager] = None,
        shipment_tracker: Optional[ShipmentTracker] = None,
        shipping_calculator: Optional[ShippingCalculator] = None,
        order_shipper: Optional[OrderShipper] = None
    ):
        # Use dependency injection for all components
        self.shipment_manager = shipment_manager or DefaultShipmentManager()
        self.shipment_tracker = shipment_tracker or DefaultShipmentTracker(self.shipment_manager)
        self.shipping_calculator = shipping_calculator or DefaultShippingCalculator()
        self.order_shipper = order_shipper or DefaultOrderShipper(self.shipment_manager, self.shipping_calculator)
    
    # Shipment management operations
    def create_shipment(self, order_id: int, shipping_method: ShippingMethod, tracking_number: str = None) -> str:
        """Create a new shipment for an order"""
        return self.shipment_manager.create_shipment(order_id, shipping_method, tracking_number)
    
    def update_shipment_status(self, shipment_id: str, status: str, location: str = None, notes: str = None) -> bool:
        """Update the status of a shipment"""
        return self.shipment_manager.update_shipment_status(shipment_id, status, location, notes)
    
    def get_shipment(self, shipment_id: str) -> Optional[Dict[str, Any]]:
        """Get shipment details by ID"""
        return self.shipment_manager.get_shipment(shipment_id)
    
    def get_shipments_by_order(self, order_id: int) -> List[Dict[str, Any]]:
        """Get all shipments for an order"""
        return self.shipment_manager.get_shipments_by_order(order_id)
    
    # Shipment tracking operations
    def track_shipment(self, tracking_number: str) -> Optional[Dict[str, Any]]:
        """Track a shipment by tracking number"""
        return self.shipment_tracker.track_shipment(tracking_number)
    
    def get_tracking_history(self, tracking_number: str) -> List[Dict[str, Any]]:
        """Get the tracking history for a shipment"""
        return self.shipment_tracker.get_tracking_history(tracking_number)
    
    # Shipping calculation operations
    def calculate_shipping_cost(self, order: Order, shipping_method: ShippingMethod, address: Address) -> Money:
        """Calculate shipping cost based on order, shipping method, and address"""
        return self.shipping_calculator.calculate_shipping_cost(order, shipping_method, address)
    
    # Order shipping operations
    def ship_order(self, order: Order, shipping_method: ShippingMethod, address: Address) -> Dict[str, Any]:
        """Ship an order and return shipment details"""
        return self.order_shipper.ship_order(order, shipping_method, address)
    
    def get_shipping_cost_estimate(self, order: Order, shipping_method: ShippingMethod, address: Address) -> Money:
        """Get an estimate of shipping cost without creating a shipment"""
        return self.order_shipper.get_shipping_cost_estimate(order, shipping_method, address)