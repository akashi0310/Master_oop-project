import datetime
from typing import Dict, List, Any
from ecommerce_order_management.domain.models.product import Product, ProductId

class InventoryService:
    def __init__(self, products: Dict[ProductId, Product], inventory_logs: List[Dict[str, Any]]):
        self.products = products
        self.inventory_logs = inventory_logs

    def log_inventory_change(self, product_id: ProductId, quantity_change: int, reason: str) -> None:
        self.inventory_logs.append({
            'product_id': product_id,
            'quantity_change': quantity_change,
            'reason': reason,
            'timestamp': datetime.datetime.now()
        })

    def deduct_stock(self, product_id: ProductId, quantity: int, order_id: int) -> bool:
        product = self.products.get(product_id)
        if not product:
            return False
        if product.quantity_available < quantity:
            return False
        product.quantity_available -= quantity
        self.log_inventory_change(product_id, -quantity, f"order_{order_id}")
        return True

    def restore_stock(self, product_id: ProductId, quantity: int, order_id: int) -> bool:
        product = self.products.get(product_id)
        if not product:
            return False
        product.quantity_available += quantity
        self.log_inventory_change(product_id, quantity, f"cancel_order_{order_id}")
        return True

    def restock_product(self, product_id: ProductId, quantity: int, supplier_id: ProductId = None) -> bool:
        product = self.products.get(product_id)
        if not product:
            return False
        # Verify supplier if provided
        if supplier_id and product.supplier_id != supplier_id:
            return False
        product.quantity_available += quantity
        self.log_inventory_change(product_id, quantity, "restock")
        return True