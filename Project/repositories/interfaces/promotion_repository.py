from typing import List, Optional
from domain.models import Promotion


class PromotionRepository:
    """Repository interface for Promotion entities"""
    
    def add(self, promotion: Promotion) -> None:
        """Add a new promotion to the repository"""
        raise NotImplementedError
    
    def get_by_id(self, promo_id: int) -> Optional[Promotion]:
        """Get a promotion by its ID"""
        raise NotImplementedError
    
    def get_by_code(self, code: str) -> Optional[Promotion]:
        """Get a promotion by its code"""
        raise NotImplementedError
    
    def get_all(self) -> List[Promotion]:
        """Get all promotions in the repository"""
        raise NotImplementedError
    
    def update(self, promotion: Promotion) -> bool:
        """Update an existing promotion"""
        raise NotImplementedError
    
    def delete(self, promo_id: int) -> bool:
        """Delete a promotion by its ID"""
        raise NotImplementedError
    
    def get_active(self) -> List[Promotion]:
        """Get all currently active promotions"""
        raise NotImplementedError
    
    def get_expired(self) -> List[Promotion]:
        """Get all expired promotions"""
        raise NotImplementedError
    
    def get_by_category(self, category: str) -> List[Promotion]:
        """Get all promotions for a specific category"""
        raise NotImplementedError