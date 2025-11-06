from typing import List, Optional
from domain.models import Supplier
from repositories.interfaces.supplier_repository import SupplierRepository


class InMemorySupplierRepository(SupplierRepository):
    """In-memory implementation of SupplierRepository"""
    
    def __init__(self):
        self._suppliers: List[Supplier] = []
    
    def add(self, supplier: Supplier) -> None:
        """Add a new supplier to the repository"""
        if any(s.supplier_id == supplier.supplier_id for s in self._suppliers):
            raise ValueError(f"Supplier with ID {supplier.supplier_id} already exists")
        self._suppliers.append(supplier)
    
    def get_by_id(self, supplier_id: int) -> Optional[Supplier]:
        """Get a supplier by their ID"""
        for supplier in self._suppliers:
            if supplier.supplier_id == supplier_id:
                return supplier
        return None
    
    def get_all(self) -> List[Supplier]:
        """Get all suppliers in the repository"""
        return self._suppliers.copy()
    
    def update(self, supplier: Supplier) -> bool:
        """Update an existing supplier"""
        for i, existing_supplier in enumerate(self._suppliers):
            if existing_supplier.supplier_id == supplier.supplier_id:
                self._suppliers[i] = supplier
                return True
        return False
    
    def delete(self, supplier_id: int) -> bool:
        """Delete a supplier by their ID"""
        for i, supplier in enumerate(self._suppliers):
            if supplier.supplier_id == supplier_id:
                del self._suppliers[i]
                return True
        return False
    
    def get_reliable(self, threshold: float = 3.5) -> List[Supplier]:
        """Get suppliers with reliability score above threshold"""
        return [s for s in self._suppliers if s.is_reliable(threshold)]
    
    def get_active(self) -> List[Supplier]:
        """Get all active suppliers"""
        return [s for s in self._suppliers if s.is_active]
    
    def search(self, query: str) -> List[Supplier]:
        """Search for suppliers by name or email"""
        query = query.lower()
        return [
            s for s in self._suppliers 
            if query in s.name.lower() or query in s.email.value.lower()
        ]