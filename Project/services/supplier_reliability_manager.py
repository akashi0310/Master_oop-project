from domain.interfaces.supplier_interfaces import SupplierReliabilityManagement


class SupplierReliabilityManager(SupplierReliabilityManagement):
    """Manages the reliability score of a supplier"""
    
    def __init__(self, initial_score: float = 0.0):
        if initial_score < 0 or initial_score > 5:
            raise ValueError("Reliability score must be between 0 and 5")
        self._reliability_score = initial_score
    
    @property
    def reliability_score(self) -> float:
        """Get the current reliability score"""
        return self._reliability_score
    
    def update_reliability_score(self, new_score: float) -> None:
        """Update the supplier's reliability score"""
        if new_score < 0 or new_score > 5:
            raise ValueError("Reliability score must be between 0 and 5")
        self._reliability_score = new_score
    
    def is_reliable(self, threshold: float = 3.5) -> bool:
        """Check if the supplier is considered reliable"""
        return self._reliability_score >= threshold