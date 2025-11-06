from typing import List, Optional
from domain.models import Customer


class CustomerRepository:
    """Repository interface for Customer entities"""
    
    def add(self, customer: Customer) -> None:
        """Add a new customer to the repository"""
        raise NotImplementedError
    
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """Get a customer by their ID"""
        raise NotImplementedError
    
    def get_all(self) -> List[Customer]:
        """Get all customers in the repository"""
        raise NotImplementedError
    
    def update(self, customer: Customer) -> bool:
        """Update an existing customer"""
        raise NotImplementedError
    
    def delete(self, customer_id: int) -> bool:
        """Delete a customer by their ID"""
        raise NotImplementedError
    
    def get_by_tier(self, tier: str) -> List[Customer]:
        """Get all customers with a specific membership tier"""
        raise NotImplementedError
    
    def get_by_email(self, email: str) -> Optional[Customer]:
        """Get a customer by their email address"""
        raise NotImplementedError
    
    def get_inactive(self, days: int = 90) -> List[Customer]:
        """Get customers who haven't placed an order in specified days"""
        raise NotImplementedError
    
    def search(self, query: str) -> List[Customer]:
        """Search for customers by name or email"""
        raise NotImplementedError