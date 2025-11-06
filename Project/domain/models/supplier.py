from typing import Optional, List
from ..value_objects.email import Email
from ..interfaces.supplier_interfaces import (
    SupplierInfo,
    SupplierProductManagement,
    SupplierReliabilityManagement,
    SupplierStatusManagement
)


class Supplier(
    SupplierInfo,
    SupplierProductManagement,
    SupplierReliabilityManagement,
    SupplierStatusManagement
):
    """
    Supplier class that follows SOLID principles by delegating responsibilities
    to specialized components through composition.
    """
    
    def __init__(
        self,
        supplier_id: int,
        name: str,
        email: str,
        reliability_score: float,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        product_manager=None,
        reliability_manager=None,
        status_manager=None
    ):
        # Validate basic supplier data
        if supplier_id <= 0:
            raise ValueError("Supplier ID must be positive")
        if not name or not name.strip():
            raise ValueError("Supplier name cannot be empty")
        
        # Set basic supplier information
        self._supplier_id = supplier_id
        self._name = name.strip()
        self._email = Email(email) if isinstance(email, str) else email
        self._phone = phone.strip() if phone else None
        self._address = address.strip() if address else None
        
        # Initialize specialized managers (dependency injection)
        from services.supplier_product_manager import SupplierProductManager
        from services.supplier_reliability_manager import SupplierReliabilityManager
        from services.supplier_status_manager import SupplierStatusManager
        
        self._product_manager = product_manager or SupplierProductManager()
        self._reliability_manager = reliability_manager or SupplierReliabilityManager(reliability_score)
        self._status_manager = status_manager or SupplierStatusManager()
    
    # Properties for SupplierInfo interface
    @property
    def supplier_id(self) -> int:
        """Get the supplier ID"""
        return self._supplier_id
    
    @property
    def name(self) -> str:
        """Get the supplier name"""
        return self._name
    
    @property
    def email(self) -> Email:
        """Get the supplier email"""
        return self._email
    
    @property
    def phone(self) -> Optional[str]:
        """Get the supplier phone"""
        return self._phone
    
    @property
    def address(self) -> Optional[str]:
        """Get the supplier address"""
        return self._address
    
    # Delegate product management to SupplierProductManager
    def add_product(self, product_id: int) -> None:
        """Add a product ID to the list of products supplied"""
        self._product_manager.add_product(product_id)
    
    def remove_product(self, product_id: int) -> None:
        """Remove a product ID from the list of products supplied"""
        self._product_manager.remove_product(product_id)
    
    def get_product_count(self) -> int:
        """Get the number of products supplied by this supplier"""
        return self._product_manager.get_product_count()
    
    def supplies_product(self, product_id: int) -> bool:
        """Check if the supplier supplies a specific product"""
        return self._product_manager.supplies_product(product_id)
    
    @property
    def products_supplied(self) -> List[int]:
        """Get the list of products supplied"""
        return self._product_manager.products_supplied
    
    # Delegate reliability management to SupplierReliabilityManager
    @property
    def reliability_score(self) -> float:
        """Get the current reliability score"""
        return self._reliability_manager.reliability_score
    
    def update_reliability_score(self, new_score: float) -> None:
        """Update the supplier's reliability score"""
        self._reliability_manager.update_reliability_score(new_score)
    
    def is_reliable(self, threshold: float = 3.5) -> bool:
        """Check if the supplier is considered reliable"""
        return self._reliability_manager.is_reliable(threshold)
    
    # Delegate status management to SupplierStatusManager
    @property
    def is_active(self) -> bool:
        """Get the current activation status"""
        return self._status_manager.is_active
    
    def activate(self) -> None:
        """Activate the supplier"""
        self._status_manager.activate()
    
    def deactivate(self) -> None:
        """Deactivate the supplier"""
        self._status_manager.deactivate()
