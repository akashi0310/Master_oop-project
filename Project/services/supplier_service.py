from typing import List, Optional, Dict, Any
from domain.models import Supplier, Product
from services.interfaces.supplier_service_interfaces import (
    SupplierRepository, 
    SupplierProductManager, 
    SupplierReliabilityManager, 
    SupplierStatusManager, 
    SupplierNotificationManager, 
    SupplierAnalytics
)


class DefaultSupplierRepository(SupplierRepository):
    """Default implementation of supplier repository"""
    def __init__(self):
        self.suppliers: List[Supplier] = []
    
    def add_supplier(self, supplier: Supplier) -> None:
        """Add a new supplier to the repository"""
        if any(s.supplier_id == supplier.supplier_id for s in self.suppliers):
            raise ValueError(f"Supplier with ID {supplier.supplier_id} already exists")
        self.suppliers.append(supplier)
    
    def get_supplier(self, supplier_id: int) -> Optional[Supplier]:
        """Get a supplier by ID"""
        for supplier in self.suppliers:
            if supplier.supplier_id == supplier_id:
                return supplier
        return None
    
    def get_all_suppliers(self) -> List[Supplier]:
        """Get all suppliers"""
        return self.suppliers.copy()
    
    def update_supplier(self, supplier: Supplier) -> bool:
        """Update a supplier in the repository"""
        existing_supplier = self.get_supplier(supplier.supplier_id)
        if existing_supplier:
            # Update the existing supplier with new information
            existing_supplier.name = supplier.name
            existing_supplier.email = supplier.email
            existing_supplier.phone = supplier.phone
            existing_supplier.is_active = supplier.is_active
            existing_supplier.reliability_score = supplier.reliability_score
            return True
        return False
    
    def remove_supplier(self, supplier_id: int) -> bool:
        """Remove a supplier from the repository"""
        for i, supplier in enumerate(self.suppliers):
            if supplier.supplier_id == supplier_id:
                del self.suppliers[i]
                return True
        return False


class DefaultSupplierProductManager(SupplierProductManager):
    """Default implementation of supplier-product relationship management"""
    def __init__(self, supplier_repository: SupplierRepository):
        self.supplier_repository = supplier_repository
    
    def add_product_to_supplier(self, supplier_id: int, product_id: int) -> bool:
        """Add a product to a supplier's list"""
        supplier = self.supplier_repository.get_supplier(supplier_id)
        if supplier:
            supplier.add_product(product_id)
            return True
        return False
    
    def remove_product_from_supplier(self, supplier_id: int, product_id: int) -> bool:
        """Remove a product from a supplier's list"""
        supplier = self.supplier_repository.get_supplier(supplier_id)
        if supplier:
            supplier.remove_product(product_id)
            return True
        return False
    
    def get_suppliers_by_product(self, product_id: int, products: List[Product]) -> List[Supplier]:
        """Get suppliers for a specific product"""
        # Find product first
        product = next((p for p in products if p.product_id == product_id), None)
        if not product:
            return []
        
        # Find suppliers that supply this product
        suppliers = self.supplier_repository.get_all_suppliers()
        return [s for s in suppliers if s.supplies_product(product_id)]


class DefaultSupplierReliabilityManager(SupplierReliabilityManager):
    """Default implementation of supplier reliability management"""
    def __init__(self, supplier_repository: SupplierRepository):
        self.supplier_repository = supplier_repository
    
    def update_supplier_reliability(self, supplier_id: int, new_score: float) -> bool:
        """Update a supplier's reliability score"""
        supplier = self.supplier_repository.get_supplier(supplier_id)
        if supplier:
            supplier.update_reliability_score(new_score)
            self.supplier_repository.update_supplier(supplier)
            return True
        return False
    
    def get_reliable_suppliers(self, threshold: float = 3.5) -> List[Supplier]:
        """Get suppliers with reliability score above threshold"""
        suppliers = self.supplier_repository.get_all_suppliers()
        return [s for s in suppliers if s.is_reliable(threshold)]


class DefaultSupplierStatusManager(SupplierStatusManager):
    """Default implementation of supplier status management"""
    def __init__(self, supplier_repository: SupplierRepository):
        self.supplier_repository = supplier_repository
    
    def activate_supplier(self, supplier_id: int) -> bool:
        """Activate a supplier"""
        supplier = self.supplier_repository.get_supplier(supplier_id)
        if supplier:
            supplier.activate()
            self.supplier_repository.update_supplier(supplier)
            return True
        return False
    
    def deactivate_supplier(self, supplier_id: int) -> bool:
        """Deactivate a supplier"""
        supplier = self.supplier_repository.get_supplier(supplier_id)
        if supplier:
            supplier.deactivate()
            self.supplier_repository.update_supplier(supplier)
            return True
        return False


class DefaultSupplierNotificationManager(SupplierNotificationManager):
    """Default implementation of supplier notifications"""
    def __init__(self, supplier_repository: SupplierRepository):
        self.supplier_repository = supplier_repository
    
    def notify_low_stock(self, product_id: int, products: List[Product]) -> List[Supplier]:
        """Notify suppliers of low stock for a product"""
        # Find product first
        product = next((p for p in products if p.product_id == product_id), None)
        if not product:
            return []
        
        # Find suppliers for this product
        suppliers = self.supplier_repository.get_all_suppliers()
        product_suppliers = [s for s in suppliers if s.supplies_product(product_id)]
        
        # In a real system, would send actual notifications here
        for supplier in product_suppliers:
            print(f"Email to {supplier.email.value}: Low stock alert for {product.name}")
        
        return product_suppliers


class DefaultSupplierAnalytics(SupplierAnalytics):
    """Default implementation of supplier analytics and reporting"""
    def __init__(self, supplier_repository: SupplierRepository):
        self.supplier_repository = supplier_repository
    
    def get_supplier_performance_report(self) -> Dict[str, Any]:
        """Generate a supplier performance report"""
        suppliers = self.supplier_repository.get_all_suppliers()
        if not suppliers:
            return {}
        
        total_suppliers = len(suppliers)
        reliable_count = len([s for s in suppliers if s.is_reliable()])
        active_count = len([s for s in suppliers if s.is_active])
        
        # Calculate average reliability score
        total_score = sum(s.reliability_score for s in suppliers)
        avg_score = total_score / total_suppliers
        
        # Count products per supplier
        supplier_product_counts = {}
        for supplier in suppliers:
            supplier_product_counts[supplier.supplier_id] = supplier.get_product_count()
        
        return {
            'total_suppliers': total_suppliers,
            'reliable_suppliers': reliable_count,
            'active_suppliers': active_count,
            'average_reliability_score': avg_score,
            'supplier_product_counts': supplier_product_counts
        }


class SupplierService:
    """
    Refactored SupplierService that follows SOLID principles by delegating
    responsibilities to appropriate components.
    """
    
    def __init__(
        self,
        supplier_repository: Optional[SupplierRepository] = None,
        product_manager: Optional[SupplierProductManager] = None,
        reliability_manager: Optional[SupplierReliabilityManager] = None,
        status_manager: Optional[SupplierStatusManager] = None,
        notification_manager: Optional[SupplierNotificationManager] = None,
        analytics: Optional[SupplierAnalytics] = None
    ):
        # Use dependency injection for all components
        self.supplier_repository = supplier_repository or DefaultSupplierRepository()
        self.product_manager = product_manager or DefaultSupplierProductManager(self.supplier_repository)
        self.reliability_manager = reliability_manager or DefaultSupplierReliabilityManager(self.supplier_repository)
        self.status_manager = status_manager or DefaultSupplierStatusManager(self.supplier_repository)
        self.notification_manager = notification_manager or DefaultSupplierNotificationManager(self.supplier_repository)
        self.analytics = analytics or DefaultSupplierAnalytics(self.supplier_repository)
    
    # Supplier repository operations
    def add_supplier(self, supplier: Supplier) -> None:
        """Add a new supplier to the system"""
        self.supplier_repository.add_supplier(supplier)
    
    def get_supplier(self, supplier_id: int) -> Optional[Supplier]:
        """Get a supplier by ID"""
        return self.supplier_repository.get_supplier(supplier_id)
    
    def get_all_suppliers(self) -> List[Supplier]:
        """Get all suppliers"""
        return self.supplier_repository.get_all_suppliers()
    
    def get_reliable_suppliers(self, threshold: float = 3.5) -> List[Supplier]:
        """Get suppliers with reliability score above threshold"""
        return self.reliability_manager.get_reliable_suppliers(threshold)
    
    def update_supplier_reliability(self, supplier_id: int, new_score: float) -> bool:
        """Update a supplier's reliability score"""
        return self.reliability_manager.update_supplier_reliability(supplier_id, new_score)
    
    def get_suppliers_by_product(self, product_id: int, products: List[Product]) -> List[Supplier]:
        """Get suppliers for a specific product"""
        return self.product_manager.get_suppliers_by_product(product_id, products)
    
    def notify_low_stock(self, product_id: int, products: List[Product]) -> List[Supplier]:
        """Notify suppliers of low stock for a product"""
        return self.notification_manager.notify_low_stock(product_id, products)
    
    def get_supplier_performance_report(self) -> Dict[str, Any]:
        """Generate a supplier performance report"""
        return self.analytics.get_supplier_performance_report()
    
    # Status management operations
    def deactivate_supplier(self, supplier_id: int) -> bool:
        """Deactivate a supplier"""
        return self.status_manager.deactivate_supplier(supplier_id)
    
    def activate_supplier(self, supplier_id: int) -> bool:
        """Activate a supplier"""
        return self.status_manager.activate_supplier(supplier_id)
    
    def remove_supplier(self, supplier_id: int) -> bool:
        """Remove a supplier from the system"""
        return self.supplier_repository.remove_supplier(supplier_id)
    
    # Product management operations
    def add_product_to_supplier(self, supplier_id: int, product_id: int) -> bool:
        """Add a product to a supplier's list"""
        return self.product_manager.add_product_to_supplier(supplier_id, product_id)
    
    def remove_product_from_supplier(self, supplier_id: int, product_id: int) -> bool:
        """Remove a product from a supplier's list"""
        return self.product_manager.remove_product_from_supplier(supplier_id, product_id)