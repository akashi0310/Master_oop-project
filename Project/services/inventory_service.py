import datetime
from typing import List, Dict, Any, Optional
from domain.models import Product
from domain.value_objects import Money
from services.interfaces.inventory_service_interfaces import (
    InventoryLogger, 
    InventoryManager
)


class DefaultInventoryLogger(InventoryLogger):
    """Default implementation of inventory logging"""
    def __init__(self):
        self.inventory_logs: List[Dict[str, Any]] = []
    
    def log_inventory_change(self, product_id: int, quantity_change: int, reason: str) -> None:
        """Log an inventory change for tracking purposes"""
        if product_id <= 0:
            raise ValueError("Product ID must be positive")
        if not reason or not reason.strip():
            raise ValueError("Reason cannot be empty")
        
        self.inventory_logs.append({
            'product_id': product_id,
            'quantity_change': quantity_change,
            'reason': reason.strip(),
            'timestamp': datetime.datetime.now()
        })
    
    def get_inventory_logs(self, product_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get inventory logs, optionally filtered by product ID"""
        if product_id is not None:
            return [log for log in self.inventory_logs if log['product_id'] == product_id]
        return self.inventory_logs.copy()
    
    def get_inventory_changes_by_date_range(self, start_date: datetime.datetime, end_date: datetime.datetime) -> List[Dict[str, Any]]:
        """Get inventory logs within a specific date range"""
        if start_date > end_date:
            raise ValueError("Start date must be before end date")
        
        return [
            log for log in self.inventory_logs
            if start_date <= log['timestamp'] <= end_date
        ]


class DefaultInventoryManager(InventoryManager):
    """Default implementation of inventory management"""
    def __init__(self, inventory_logger: InventoryLogger):
        self.inventory_logger = inventory_logger
    
    def restock_product(self, product: Product, quantity: int, reason: str = "restock") -> None:
        """Restock a product and log the change"""
        if quantity <= 0:
            raise ValueError("Restock quantity must be positive")
        
        product.increase_stock(quantity)
        self.inventory_logger.log_inventory_change(product.product_id, quantity, reason)
    
    def deduct_stock(self, product: Product, quantity: int, reason: str = "order") -> None:
        """Deduct stock from a product and log the change"""
        if quantity <= 0:
            raise ValueError("Deduct quantity must be positive")
        
        product.reduce_stock(quantity)
        self.inventory_logger.log_inventory_change(product.product_id, -quantity, reason)
    
    def get_low_stock_products(self, products: List[Product], threshold: int = 10) -> List[Product]:
        """Get products with stock below the threshold"""
        if threshold < 0:
            raise ValueError("Threshold cannot be negative")
        
        return [product for product in products if product.is_low_stock(threshold)]
    
    def get_out_of_stock_products(self, products: List[Product]) -> List[Product]:
        """Get products that are out of stock"""
        return [product for product in products if not product.is_in_stock()]
    
    def get_total_inventory_value(self, products: List[Product]) -> Money:
        """Calculate the total value of all inventory"""
        total_value = Money(0.0)
        for product in products:
            total_value = total_value.add(product.get_total_value())
        return total_value


class InventoryService:
    """
    Refactored InventoryService that follows SOLID principles by delegating
    responsibilities to appropriate components.
    """
    
    def __init__(
        self,
        inventory_logger: Optional[InventoryLogger] = None,
        inventory_manager: Optional[InventoryManager] = None
    ):
        # Use dependency injection for all components
        self.inventory_logger = inventory_logger or DefaultInventoryLogger()
        self.inventory_manager = inventory_manager or DefaultInventoryManager(self.inventory_logger)
    
    # Inventory logging operations
    def log_inventory_change(self, product_id: int, quantity_change: int, reason: str) -> None:
        """Log an inventory change for tracking purposes"""
        self.inventory_logger.log_inventory_change(product_id, quantity_change, reason)
    
    def get_inventory_logs(self, product_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get inventory logs, optionally filtered by product ID"""
        return self.inventory_logger.get_inventory_logs(product_id)
    
    def get_inventory_changes_by_date_range(self, start_date: datetime.datetime, end_date: datetime.datetime) -> List[Dict[str, Any]]:
        """Get inventory logs within a specific date range"""
        return self.inventory_logger.get_inventory_changes_by_date_range(start_date, end_date)
    
    # Inventory management operations
    def restock_product(self, product: Product, quantity: int, reason: str = "restock") -> None:
        """Restock a product and log the change"""
        self.inventory_manager.restock_product(product, quantity, reason)
    
    def deduct_stock(self, product: Product, quantity: int, reason: str = "order") -> None:
        """Deduct stock from a product and log the change"""
        self.inventory_manager.deduct_stock(product, quantity, reason)
    
    def get_low_stock_products(self, products: List[Product], threshold: int = 10) -> List[Product]:
        """Get products with stock below the threshold"""
        return self.inventory_manager.get_low_stock_products(products, threshold)
    
    def get_out_of_stock_products(self, products: List[Product]) -> List[Product]:
        """Get products that are out of stock"""
        return self.inventory_manager.get_out_of_stock_products(products)
    
    def get_total_inventory_value(self, products: List[Product]) -> Money:
        """Calculate the total value of all inventory"""
        return self.inventory_manager.get_total_inventory_value(products)