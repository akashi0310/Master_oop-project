from typing import List, Optional, Dict, Any
from domain.models import Supplier, Product


class SupplierRepository:
    """Interface for supplier repository operations"""
    def add_supplier(self, supplier: Supplier) -> None:
        """Add a new supplier to the repository"""
        pass
    
    def get_supplier(self, supplier_id: int) -> Optional[Supplier]:
        """Get a supplier by ID"""
        pass
    
    def get_all_suppliers(self) -> List[Supplier]:
        """Get all suppliers"""
        pass
    
    def update_supplier(self, supplier: Supplier) -> bool:
        """Update a supplier in the repository"""
        pass
    
    def remove_supplier(self, supplier_id: int) -> bool:
        """Remove a supplier from the repository"""
        pass


class SupplierProductManager:
    """Interface for managing supplier-product relationships"""
    def add_product_to_supplier(self, supplier_id: int, product_id: int) -> bool:
        """Add a product to a supplier's list"""
        pass
    
    def remove_product_from_supplier(self, supplier_id: int, product_id: int) -> bool:
        """Remove a product from a supplier's list"""
        pass
    
    def get_suppliers_by_product(self, product_id: int, products: List[Product]) -> List[Supplier]:
        """Get suppliers for a specific product"""
        pass


class SupplierReliabilityManager:
    """Interface for managing supplier reliability"""
    def update_supplier_reliability(self, supplier_id: int, new_score: float) -> bool:
        """Update a supplier's reliability score"""
        pass
    
    def get_reliable_suppliers(self, threshold: float = 3.5) -> List[Supplier]:
        """Get suppliers with reliability score above threshold"""
        pass


class SupplierStatusManager:
    """Interface for managing supplier status"""
    def activate_supplier(self, supplier_id: int) -> bool:
        """Activate a supplier"""
        pass
    
    def deactivate_supplier(self, supplier_id: int) -> bool:
        """Deactivate a supplier"""
        pass


class SupplierNotificationManager:
    """Interface for supplier notifications"""
    def notify_low_stock(self, product_id: int, products: List[Product]) -> List[Supplier]:
        """Notify suppliers of low stock for a product"""
        pass


class SupplierAnalytics:
    """Interface for supplier analytics and reporting"""
    def get_supplier_performance_report(self) -> Dict[str, Any]:
        """Generate a supplier performance report"""
        pass