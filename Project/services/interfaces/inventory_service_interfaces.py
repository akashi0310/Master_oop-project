from typing import List, Dict, Any, Optional
from datetime import datetime
from domain.models import Product
from domain.value_objects import Money


class InventoryLogger:
    """Interface for inventory logging"""
    def log_inventory_change(self, product_id: int, quantity_change: int, reason: str) -> None:
        """Log an inventory change for tracking purposes"""
        pass
    
    def get_inventory_logs(self, product_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get inventory logs, optionally filtered by product ID"""
        pass
    
    def get_inventory_changes_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get inventory logs within a specific date range"""
        pass


class InventoryManager:
    """Interface for inventory management operations"""
    def restock_product(self, product: Product, quantity: int, reason: str = "restock") -> None:
        """Restock a product and log the change"""
        pass
    
    def deduct_stock(self, product: Product, quantity: int, reason: str = "order") -> None:
        """Deduct stock from a product and log the change"""
        pass
    
    def get_low_stock_products(self, products: List[Product], threshold: int = 10) -> List[Product]:
        """Get products with stock below the threshold"""
        pass
    
    def get_out_of_stock_products(self, products: List[Product]) -> List[Product]:
        """Get products that are out of stock"""
        pass
    
    def get_total_inventory_value(self, products: List[Product]) -> Money:
        """Calculate the total value of all inventory"""
        pass