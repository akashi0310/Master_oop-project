from typing import List, Optional
from ..value_objects.email import Email


class Supplier:
    def __init__(
        self,
        supplier_id: int,
        name: str,
        email: str,
        reliability_score: float,
        phone: Optional[str] = None,
        address: Optional[str] = None
    ):
        if supplier_id <= 0:
            raise ValueError("Supplier ID must be positive")
        if not name or not name.strip():
            raise ValueError("Supplier name cannot be empty")
        if reliability_score < 0 or reliability_score > 5:
            raise ValueError("Reliability score must be between 0 and 5")
        
        self.supplier_id = supplier_id
        self.name = name.strip()
        self.email = Email(email) if isinstance(email, str) else email
        self.reliability_score = reliability_score
        self.phone = phone.strip() if phone else None
        self.address = address.strip() if address else None
        self.products_supplied: List[int] = []  # List of product IDs
        self.is_active = True
    
    def add_product(self, product_id: int) -> None:
        """Add a product ID to the list of products supplied"""
        if product_id <= 0:
            raise ValueError("Product ID must be positive")
        if product_id not in self.products_supplied:
            self.products_supplied.append(product_id)
    
    def remove_product(self, product_id: int) -> None:
        """Remove a product ID from the list of products supplied"""
        if product_id in self.products_supplied:
            self.products_supplied.remove(product_id)
    
    def update_reliability_score(self, new_score: float) -> None:
        """Update the supplier's reliability score"""
        if new_score < 0 or new_score > 5:
            raise ValueError("Reliability score must be between 0 and 5")
        self.reliability_score = new_score
    
    def is_reliable(self, threshold: float = 3.5) -> bool:
        """Check if the supplier is considered reliable"""
        return self.reliability_score >= threshold
    
    def deactivate(self) -> None:
        """Deactivate the supplier"""
        self.is_active = False
    
    def activate(self) -> None:
        """Activate the supplier"""
        self.is_active = True
    
    def get_product_count(self) -> int:
        """Get the number of products supplied by this supplier"""
        return len(self.products_supplied)
    
    def supplies_product(self, product_id: int) -> bool:
        """Check if the supplier supplies a specific product"""
        return product_id in self.products_supplied
