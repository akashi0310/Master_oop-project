from domain.interfaces.customer_interfaces import CustomerValidator


class DefaultCustomerValidator(CustomerValidator):
    """Default implementation of customer validation"""
    
    def validate_customer_data(self, customer_id: int, name: str, loyalty_points: int) -> None:
        """Validate basic customer data"""
        if not name or not name.strip():
            raise ValueError("Customer name cannot be empty")
        if customer_id <= 0:
            raise ValueError("Customer ID must be positive")
        if loyalty_points < 0:
            raise ValueError("Loyalty points cannot be negative")