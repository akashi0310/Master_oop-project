from typing import List, Optional
from domain.models import Customer, Order
from domain.enums import MembershipTier
from domain.value_objects import Money


class CustomerRepository:
    """Interface for customer repository operations"""
    def add_customer(self, customer: Customer) -> None:
        """Add a new customer to the repository"""
        pass
    
    def get_customer(self, customer_id: int) -> Optional[Customer]:
        """Get a customer by ID"""
        pass
    
    def get_all_customers(self) -> List[Customer]:
        """Get all customers"""
        pass
    
    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Get a customer by email"""
        pass
    
    def update_customer(self, customer: Customer) -> bool:
        """Update customer information"""
        pass
    
    def remove_customer(self, customer_id: int) -> bool:
        """Remove a customer from the repository"""
        pass


class CustomerLoyaltyManager:
    """Interface for managing customer loyalty points"""
    def add_loyalty_points(self, customer_id: int, points: int) -> bool:
        """Add loyalty points to a customer's account"""
        pass
    
    def redeem_loyalty_points(self, customer_id: int, points: int) -> bool:
        """Redeem loyalty points from a customer's account"""
        pass


class CustomerMembershipManager:
    """Interface for managing customer membership"""
    def upgrade_membership(self, customer_id: int, new_tier: MembershipTier) -> bool:
        """Upgrade a customer's membership tier"""
        pass
    
    def get_membership_discount_rate(self, customer_id: int) -> float:
        """Get the discount rate for a customer's membership tier"""
        pass


class CustomerAnalytics:
    """Interface for customer analytics and reporting"""
    def get_customer_lifetime_value(self, customer_id: int, orders: List[Order]) -> Money:
        """Calculate lifetime value of a customer"""
        pass
    
    def get_top_customers(self, orders: List[Order], limit: int = 10) -> List[tuple[Customer, Money]]:
        """Get top customers by lifetime value"""
        pass
    
    def get_inactive_customers(self, days: int = 90) -> List[Customer]:
        """Get customers who haven't placed an order in specified days"""
        pass