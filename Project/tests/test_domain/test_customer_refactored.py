import unittest
from domain.models.customer import Customer
from domain.value_objects.email import Email
from domain.value_objects.address import Address
from domain.enums.membership_tier import MembershipTier
from services.customer_validator import DefaultCustomerValidator


class TestCustomerRefactored(unittest.TestCase):
    """Test cases for the refactored Customer class"""
    
    def test_customer_creation(self):
        """Test creating a customer with valid data"""
        customer = Customer(
            customer_id=1,
            name="John Doe",
            email="john@example.com",
            membership_tier="gold",
            phone="123-456-7890",
            address="123 Main St, Anytown CA 12345",
            loyalty_points=100
        )
        
        self.assertEqual(customer.customer_id, 1)
        self.assertEqual(customer.name, "John Doe")
        self.assertEqual(str(customer.email), "john@example.com")
        self.assertEqual(customer.membership_tier, MembershipTier.GOLD)
        self.assertEqual(customer.phone, "123-456-7890")
        self.assertEqual(str(customer.address), "123 Main St, Anytown, CA 12345")
        self.assertEqual(customer.loyalty_points, 100)
        self.assertEqual(customer.order_history, [])
    
    def test_customer_with_value_objects(self):
        """Test creating a customer with value objects"""
        email = Email("jane@example.com")
        address = Address("456 Oak Ave", "Smalltown", "TX", "67890")
        
        customer = Customer(
            customer_id=2,
            name="Jane Smith",
            email=email,
            membership_tier=MembershipTier.SILVER,
            address=address
        )
        
        self.assertEqual(customer.email, email)
        self.assertEqual(customer.address, address)
        self.assertEqual(customer.membership_tier, MembershipTier.SILVER)
    
    def test_loyalty_points_operations(self):
        """Test loyalty points operations"""
        customer = Customer(
            customer_id=3,
            name="Bob Johnson",
            email="bob@example.com",
            membership_tier=MembershipTier.BRONZE,
            loyalty_points=50
        )
        
        # Test adding points (bronze gets 1.2x multiplier)
        customer.add_loyalty_points(10)
        self.assertEqual(customer.loyalty_points, 62)  # 50 + (10 * 1.2)
        
        # Test redeeming points
        success = customer.redeem_loyalty_points(20)
        self.assertTrue(success)
        self.assertEqual(customer.loyalty_points, 42)
        
        # Test redeeming more points than available
        success = customer.redeem_loyalty_points(50)
        self.assertFalse(success)
        self.assertEqual(customer.loyalty_points, 42)
    
    def test_membership_operations(self):
        """Test membership operations"""
        customer = Customer(
            customer_id=4,
            name="Alice Brown",
            email="alice@example.com",
            membership_tier=MembershipTier.STANDARD
        )
        
        # Test membership discount rates
        self.assertEqual(customer.get_membership_discount_rate(), 0.0)
        self.assertEqual(customer.get_shipping_discount_rate(), 0.0)
        self.assertTrue(customer.can_place_order())
        
        # Test upgrading membership
        customer.upgrade_membership(MembershipTier.GOLD)
        self.assertEqual(customer.membership_tier, MembershipTier.GOLD)
        self.assertEqual(customer.get_membership_discount_rate(), 0.15)
        self.assertEqual(customer.get_shipping_discount_rate(), 0.5)
        
        # Test upgrading to suspended (should raise error)
        with self.assertRaises(ValueError) as context:
            customer.upgrade_membership(MembershipTier.SUSPENDED)
        self.assertIn("Cannot upgrade to suspended status", str(context.exception))
    
    def test_order_history_operations(self):
        """Test order history operations"""
        customer = Customer(
            customer_id=5,
            name="Charlie Wilson",
            email="charlie@example.com",
            membership_tier=MembershipTier.SILVER
        )
        
        # Test adding orders to history
        customer.add_order_to_history(101)
        customer.add_order_to_history(102)
        self.assertEqual(customer.order_history, [101, 102])
        
        # Test adding invalid order ID
        with self.assertRaises(ValueError) as context:
            customer.add_order_to_history(-1)
        self.assertIn("Order ID must be positive", str(context.exception))
    
    def test_customer_validation(self):
        """Test customer validation"""
        # Test invalid customer ID
        with self.assertRaises(ValueError) as context:
            Customer(
                customer_id=0,
                name="Test User",
                email="test@example.com",
                membership_tier=MembershipTier.STANDARD
            )
        self.assertIn("Customer ID must be positive", str(context.exception))
        
        # Test empty name
        with self.assertRaises(ValueError) as context:
            Customer(
                customer_id=1,
                name="",
                email="test@example.com",
                membership_tier=MembershipTier.STANDARD
            )
        self.assertIn("Customer name cannot be empty", str(context.exception))
        
        # Test negative loyalty points
        with self.assertRaises(ValueError) as context:
            Customer(
                customer_id=1,
                name="Test User",
                email="test@example.com",
                membership_tier=MembershipTier.STANDARD,
                loyalty_points=-10
            )
        self.assertIn("Loyalty points cannot be negative", str(context.exception))
    
    def test_custom_validator(self):
        """Test using a custom validator"""
        class StrictValidator(DefaultCustomerValidator):
            def validate_customer_data(self, customer_id: int, name: str, loyalty_points: int) -> None:
                super().validate_customer_data(customer_id, name, loyalty_points)
                if len(name) < 5:
                    raise ValueError("Name must be at least 5 characters long")
        
        # Test with valid data
        customer = Customer(
            customer_id=6,
            name="Valid Name",
            email="valid@example.com",
            membership_tier=MembershipTier.STANDARD,
            validator=StrictValidator()
        )
        self.assertEqual(customer.name, "Valid Name")
        
        # Test with invalid data for custom validator
        with self.assertRaises(ValueError) as context:
            Customer(
                customer_id=7,
                name="Bob",
                email="bob@example.com",
                membership_tier=MembershipTier.STANDARD,
                validator=StrictValidator()
            )
        self.assertIn("Name must be at least 5 characters long", str(context.exception))


if __name__ == '__main__':
    unittest.main()