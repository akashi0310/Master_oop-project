from typing import List, Optional, Dict, Any
from domain.models import Supplier, Product


class SupplierService:
    def __init__(self, supplier_repository=None):
        self.supplier_repository = supplier_repository
        self.suppliers: List[Supplier] = []
    
    def add_supplier(self, supplier: Supplier) -> None:
        """Add a new supplier to the system"""
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
    
    def get_reliable_suppliers(self, threshold: float = 3.5) -> List[Supplier]:
        """Get suppliers with reliability score above threshold"""
        return [s for s in self.suppliers if s.is_reliable(threshold)]
    
    def update_supplier_reliability(self, supplier_id: int, new_score: float) -> bool:
        """Update a supplier's reliability score"""
        supplier = self.get_supplier(supplier_id)
        if supplier:
            supplier.update_reliability_score(new_score)
            return True
        return False
    
    def get_suppliers_by_product(self, product_id: int, products: List[Product]) -> List[Supplier]:
        """Get suppliers for a specific product"""
        # Find the product first
        product = next((p for p in products if p.product_id == product_id), None)
        if not product:
            return []
        
        # Find suppliers that supply this product
        return [s for s in self.suppliers if s.supplies_product(product_id)]
    
    def notify_low_stock(self, product_id: int, products: List[Product]) -> List[Supplier]:
        """Notify suppliers of low stock for a product"""
        # Find the product first
        product = next((p for p in products if p.product_id == product_id), None)
        if not product:
            return []
        
        # Find suppliers for this product
        suppliers = self.get_suppliers_by_product(product_id, products)
        
        # In a real system, would send actual notifications here
        for supplier in suppliers:
            print(f"Email to {supplier.email.value}: Low stock alert for {product.name}")
        
        return suppliers
    
    def get_supplier_performance_report(self) -> Dict[str, Any]:
        """Generate a supplier performance report"""
        if not self.suppliers:
            return {}
        
        total_suppliers = len(self.suppliers)
        reliable_count = len([s for s in self.suppliers if s.is_reliable()])
        active_count = len([s for s in self.suppliers if s.is_active])
        
        # Calculate average reliability score
        total_score = sum(s.reliability_score for s in self.suppliers)
        avg_score = total_score / total_suppliers
        
        # Count products per supplier
        supplier_product_counts = {}
        for supplier in self.suppliers:
            supplier_product_counts[supplier.supplier_id] = supplier.get_product_count()
        
        return {
            'total_suppliers': total_suppliers,
            'reliable_suppliers': reliable_count,
            'active_suppliers': active_count,
            'average_reliability_score': avg_score,
            'supplier_product_counts': supplier_product_counts
        }
    
    def deactivate_supplier(self, supplier_id: int) -> bool:
        """Deactivate a supplier"""
        supplier = self.get_supplier(supplier_id)
        if supplier:
            supplier.deactivate()
            return True
        return False
    
    def activate_supplier(self, supplier_id: int) -> bool:
        """Activate a supplier"""
        supplier = self.get_supplier(supplier_id)
        if supplier:
            supplier.activate()
            return True
        return False
    
    def remove_supplier(self, supplier_id: int) -> bool:
        """Remove a supplier from the system"""
        for i, supplier in enumerate(self.suppliers):
            if supplier.supplier_id == supplier_id:
                del self.suppliers[i]
                return True
        return False
    
    def add_product_to_supplier(self, supplier_id: int, product_id: int) -> bool:
        """Add a product to a supplier's list"""
        supplier = self.get_supplier(supplier_id)
        if supplier:
            supplier.add_product(product_id)
            return True
        return False
    
    def remove_product_from_supplier(self, supplier_id: int, product_id: int) -> bool:
        """Remove a product from a supplier's list"""
        supplier = self.get_supplier(supplier_id)
        if supplier:
            supplier.remove_product(product_id)
            return True
        return False
