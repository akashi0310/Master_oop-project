import datetime
from typing import List, Dict, Any, Optional
from domain.models import Product


class InventoryService:
    def __init__(self, product_repository=None):
        self.product_repository = product_repository
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
    
    def restock_product(self, product: Product, quantity: int, reason: str = "restock") -> None:
        """Restock a product and log the change"""
        if quantity <= 0:
            raise ValueError("Restock quantity must be positive")
        
        product.increase_stock(quantity)
        self.log_inventory_change(product.product_id, quantity, reason)
    
    def deduct_stock(self, product: Product, quantity: int, reason: str = "order") -> None:
        """Deduct stock from a product and log the change"""
        if quantity <= 0:
            raise ValueError("Deduct quantity must be positive")
        
        product.reduce_stock(quantity)
        self.log_inventory_change(product.product_id, -quantity, reason)
    
    def get_low_stock_products(self, products: List[Product], threshold: int = 10) -> List[Product]:
        """Get products with stock below the threshold"""
        if threshold < 0:
            raise ValueError("Threshold cannot be negative")
        
        return [product for product in products if product.is_low_stock(threshold)]
    
    def get_out_of_stock_products(self, products: List[Product]) -> List[Product]:
        """Get products that are out of stock"""
        return [product for product in products if not product.is_in_stock()]
    
    def get_total_inventory_value(self, products: List[Product]) -> float:
        """Calculate the total value of all inventory"""
        total_value = 0.0
        for product in products:
            total_value += product.get_total_value().amount
        return total_value
    
    def get_inventory_changes_by_date_range(self, start_date: datetime.datetime, end_date: datetime.datetime) -> List[Dict[str, Any]]:
        """Get inventory logs within a specific date range"""
        if start_date > end_date:
            raise ValueError("Start date must be before end date")
        
        return [
            log for log in self.inventory_logs
            if start_date <= log['timestamp'] <= end_date
        ]
