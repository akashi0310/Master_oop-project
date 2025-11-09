from typing import Dict, List
from ecommerce_order_management.domain.models.supplier import Supplier, SupplierId
from ecommerce_order_management.domain.value_objects.email import Email
from ecommerce_order_management.domain.models.product import ProductId

class SupplierService:
    def __init__(self, suppliers: Dict[SupplierId, Supplier]):
        self.suppliers = suppliers

    def add_supplier(self, supplier_id: SupplierId, name: str, email: Email, reliability: float) -> None:
        self.suppliers[supplier_id] = Supplier(supplier_id, name, email, reliability)

    def get_supplier(self, supplier_id: SupplierId) -> Supplier | None:
        return self.suppliers.get(supplier_id)

    def notify_supplier_reorder(self, product_id: ProductId, supplier_id: SupplierId) -> None:
        # This method would typically interact with a NotificationService
        # For now, it will just print a message as in the original system
        supplier = self.get_supplier(supplier_id)
        if supplier:
            print(f"Email to {supplier.email}: Low stock alert for product {product_id}")