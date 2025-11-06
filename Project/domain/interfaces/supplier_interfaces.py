from typing import List, Protocol, Optional
from ..value_objects.email import Email


class SupplierInfo(Protocol):
    """Protocol for basic supplier information"""
    @property
    def supplier_id(self) -> int: ...
    
    @property
    def name(self) -> str: ...
    
    @property
    def email(self) -> Email: ...
    
    @property
    def phone(self) -> Optional[str]: ...
    
    @property
    def address(self) -> Optional[str]: ...


class SupplierProductManagement(Protocol):
    """Protocol for supplier product management operations"""
    def add_product(self, product_id: int) -> None: ...
    
    def remove_product(self, product_id: int) -> None: ...
    
    def get_product_count(self) -> int: ...
    
    def supplies_product(self, product_id: int) -> bool: ...


class SupplierReliabilityManagement(Protocol):
    """Protocol for supplier reliability management"""
    @property
    def reliability_score(self) -> float: ...
    
    def update_reliability_score(self, new_score: float) -> None: ...
    
    def is_reliable(self, threshold: float = 3.5) -> bool: ...


class SupplierStatusManagement(Protocol):
    """Protocol for supplier status management"""
    @property
    def is_active(self) -> bool: ...
    
    def activate(self) -> None: ...
    
    def deactivate(self) -> None: ...