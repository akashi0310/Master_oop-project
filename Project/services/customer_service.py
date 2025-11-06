from typing import List, Optional
from domain.models import Customer, Order
from domain.enums import MembershipTier
from domain.value_objects import Money


class CustomerService:
    def __init__(self, customer_repository=None):
        self.customer_repository = customer_repository
        self.customers: List[Customer] = []
    
    def add_customer(self, customer: Customer) -> None:
        """Add a new customer to the system"""
        if any(c.customer_id == customer.customer_id for c in self.customers):
            raise ValueError(f"Customer with ID {customer.customer_id} already exists")
        self.customers.append(customer)
    
    def get_customer(self, customer_id: int) -> Optional[Customer]:
        """Get a customer by ID"""
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        return None
    
    def get_all_customers(self) -> List[Customer]:
        """Get all customers"""
        return self.customers.copy()
    
    def get_customers_by_tier(self, tier: MembershipTier) -> List[Customer]:
        """Get customers by membership tier"""
        return [c for c in self.customers if c.membership_tier == tier]
    
    def update_customer_info(self, customer_id: int, name: Optional[str] = None, 
                           phone: Optional[str] = None, address: Optional[str] = None) -> bool:
        """Update customer information"""
        customer = self.get_customer(customer_id)
        if customer:
            if name:
                customer.name = name.strip()
            if phone:
                customer.phone = phone.strip()
            if address:
                from ..domain.value_objects import Address
                customer.address = Address.from_string(address)
            return True
        return False
    
    def add_loyalty_points(self, customer_id: int, points: int) -> bool:
        """Add loyalty points to a customer's account"""
        customer = self.get_customer(customer_id)
        if customer:
            customer.add_loyalty_points(points)
            return True
        return False
    
    def redeem_loyalty_points(self, customer_id: int, points: int) -> bool:
        """Redeem loyalty points from a customer's account"""
        customer = self.get_customer(customer_id)
        if customer:
            return customer.redeem_loyalty_points(points)
        return False
    
    def upgrade_membership(self, customer_id: int, new_tier: MembershipTier) -> bool:
        """Upgrade a customer's membership tier"""
        customer = self.get_customer(customer_id)
        if customer:
            customer.upgrade_membership(new_tier)
            return True
        return False
    
    def get_customer_lifetime_value(self, customer_id: int, orders: List[Order]) -> Money:
        """Calculate the lifetime value of a customer"""
        customer = self.get_customer(customer_id)
        if not customer:
            return Money(0.0)
        
        total_value = Money(0.0)
        for order_id in customer.order_history:
            for order in orders:
                if order.order_id == order_id and order.status.value != 'cancelled':
                    total_value = total_value.add(order.total_price)
        
        return total_value
    
    def get_top_customers(self, orders: List[Order], limit: int = 10) -> List[tuple[Customer, Money]]:
        """Get top customers by lifetime value"""
        customer_values = []
        for customer in self.customers:
            ltv = self.get_customer_lifetime_value(customer.customer_id, orders)
            customer_values.append((customer, ltv))
        
        # Sort by lifetime value (descending)
        customer_values.sort(key=lambda x: x[1].amount, reverse=True)
        return customer_values[:limit]
    
    def get_inactive_customers(self, days: int = 90) -> List[Customer]:
        """Get customers who haven't placed an order in the specified days"""
        # This would need order information with dates
        # For now, return customers with empty order history
        return [c for c in self.customers if not c.order_history]
    
    def can_customer_place_order(self, customer_id: int) -> bool:
        """Check if a customer can place orders"""
        customer = self.get_customer(customer_id)
        if customer:
            return customer.can_place_order()
        return False
    
    def add_order_to_history(self, customer_id: int, order_id: int) -> bool:
        """Add an order to a customer's history"""
        customer = self.get_customer(customer_id)
        if customer:
            customer.add_order_to_history(order_id)
            return True
        return False
    
    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Get a customer by email"""
        for customer in self.customers:
            if customer.email.value == email:
                return customer
        return None
    
    def remove_customer(self, customer_id: int) -> bool:
        """Remove a customer from the system"""
        for i, customer in enumerate(self.customers):
            if customer.customer_id == customer_id:
                del self.customers[i]
                return True
        return False
