from typing import List, Optional
from datetime import datetime, timedelta
from domain.models import Customer
from repositories.interfaces.customer_repository import CustomerRepository


class InMemoryCustomerRepository(CustomerRepository):
    """In-memory implementation of CustomerRepository"""
    
    def __init__(self):
        self._customers: List[Customer] = []
    
    def add(self, customer: Customer) -> None:
        """Add a new customer to the repository"""
        if any(c.customer_id == customer.customer_id for c in self._customers):
            raise ValueError(f"Customer with ID {customer.customer_id} already exists")
        self._customers.append(customer)
    
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """Get a customer by their ID"""
        for customer in self._customers:
            if customer.customer_id == customer_id:
                return customer
        return None
    
    def get_all(self) -> List[Customer]:
        """Get all customers in the repository"""
        return self._customers.copy()
    
    def update(self, customer: Customer) -> bool:
        """Update an existing customer"""
        for i, existing_customer in enumerate(self._customers):
            if existing_customer.customer_id == customer.customer_id:
                self._customers[i] = customer
                return True
        return False
    
    def delete(self, customer_id: int) -> bool:
        """Delete a customer by their ID"""
        for i, customer in enumerate(self._customers):
            if customer.customer_id == customer_id:
                del self._customers[i]
                return True
        return False
    
    def get_by_tier(self, tier: str) -> List[Customer]:
        """Get all customers with a specific membership tier"""
        return [c for c in self._customers if c.membership_tier.value == tier.lower()]
    
    def get_by_email(self, email: str) -> Optional[Customer]:
        """Get a customer by their email address"""
        for customer in self._customers:
            if customer.email.value == email:
                return customer
        return None
    
    def get_inactive(self, days: int = 90) -> List[Customer]:
        """Get customers who haven't placed an order in specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        inactive_customers = []
        
        for customer in self._customers:
            # Check if customer has any orders in the specified period
            has_recent_order = False
            for order_id in customer.order_history:
                # In a real implementation, would check order dates
                # For now, just check if there are any orders
                if order_id > 0:
                    has_recent_order = True
                    break
            
            if not has_recent_order:
                inactive_customers.append(customer)
        
        return inactive_customers
    
    def search(self, query: str) -> List[Customer]:
        """Search for customers by name or email"""
        query = query.lower()
        return [
            c for c in self._customers 
            if query in c.name.lower() or query in c.email.value.lower()
        ]