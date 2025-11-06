from domain.interfaces.supplier_interfaces import SupplierStatusManagement


class SupplierStatusManager(SupplierStatusManagement):
    """Manages the activation status of a supplier"""
    
    def __init__(self, initial_status: bool = True):
        self._is_active = initial_status
    
    @property
    def is_active(self) -> bool:
        """Get the current activation status"""
        return self._is_active
    
    def activate(self) -> None:
        """Activate the supplier"""
        self._is_active = True
    
    def deactivate(self) -> None:
        """Deactivate the supplier"""
        self._is_active = False