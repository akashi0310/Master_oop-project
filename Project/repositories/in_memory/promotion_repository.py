from typing import List, Optional
from domain.models import Promotion
from repositories.interfaces.promotion_repository import PromotionRepository


class InMemoryPromotionRepository(PromotionRepository):
    """In-memory implementation of PromotionRepository"""
    
    def __init__(self):
        self._promotions: List[Promotion] = []
    
    def add(self, promotion: Promotion) -> None:
        """Add a new promotion to the repository"""
        if any(p.promo_id == promotion.promo_id for p in self._promotions):
            raise ValueError(f"Promotion with ID {promotion.promo_id} already exists")
        self._promotions.append(promotion)
    
    def get_by_id(self, promo_id: int) -> Optional[Promotion]:
        """Get a promotion by its ID"""
        for promotion in self._promotions:
            if promotion.promo_id == promo_id:
                return promotion
        return None
    
    def get_by_code(self, code: str) -> Optional[Promotion]:
        """Get a promotion by its code"""
        for promotion in self._promotions:
            if promotion.code == code.upper():
                return promotion
        return None
    
    def get_all(self) -> List[Promotion]:
        """Get all promotions in the repository"""
        return self._promotions.copy()
    
    def update(self, promotion: Promotion) -> bool:
        """Update an existing promotion"""
        for i, existing_promotion in enumerate(self._promotions):
            if existing_promotion.promo_id == promotion.promo_id:
                self._promotions[i] = promotion
                return True
        return False
    
    def delete(self, promo_id: int) -> bool:
        """Delete a promotion by its ID"""
        for i, promotion in enumerate(self._promotions):
            if promotion.promo_id == promo_id:
                del self._promotions[i]
                return True
        return False
    
    def get_active(self) -> List[Promotion]:
        """Get all currently active promotions"""
        return [p for p in self._promotions if p.is_valid()]
    
    def get_expired(self) -> List[Promotion]:
        """Get all expired promotions"""
        return [p for p in self._promotions if p.is_expired()]
    
    def get_by_category(self, category: str) -> List[Promotion]:
        """Get all promotions for a specific category"""
        return [p for p in self._promotions if p.is_applicable_to_category(category)]