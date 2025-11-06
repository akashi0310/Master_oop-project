from typing import List, Optional
from domain.models import Supplier


class SupplierRepository:
    """Repository interface for Supplier entities"""
    
    def add(self, supplier: Supplier) -> None:
        """Add a new supplier to the repository"""
        raise NotImplementedError
    
    def get_by_id(self, supplier_id: int) -> Optional[Supplier]:
        """Get a supplier by their ID"""
        raise NotImplementedError
    
    def get_all(self) -> List[Supplier]:
        """Get all suppliers in the repository"""
        raise NotImplementedError
    
    def update(self, supplier: Supplier) -> bool:
        """Update an existing supplier"""
        raise NotImplementedError
    
    def delete(self, supplier_id: int) -> bool:
        """Delete a supplier by their ID"""
        raise NotImplementedError
    
    def get_reliable(self, threshold: float = 3.5) -> List[Supplier]:
        """Get suppliers with reliability score above threshold"""
        raise NotImplementedError
    
    def get_active(self) -> List[Supplier]:
        """Get all active suppliers"""
        raise NotImplementedError
    
    def search(self, query: str) -> List[Supplier]:
        """Search for suppliers by name or email"""
        raise NotImplementedError