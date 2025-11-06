import unittest
from datetime import datetime

from domain.models import Customer
from domain.enums import MembershipTier
from domain.value_objects import Email, Address


class TestCustomer(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.customer_gold = Customer(
            customer_id=101,
            name="Alice Smith",
            email="alice@email.com",
            membership_tier="gold",
            phone="555-0101",
            address="123 Main St, San Francisco CA 94102",
            loyalty_points=100
        )
        
        self.customer_silver = Customer(
            customer_id=102,
            name="Bob Jones",
            email="bob@email.com",
            membership_tier="silver",
            phone="555-0102",
            address="456 Oak Ave, New York NY 10001",
            loyalty_points=50
        )
        
        self.customer_standard = Customer(
            customer_id=103,
            name="Charlie Brown",
            email="charlie@email.com",
            membership_tier="standard",
            phone="555-0103",
            address="789 Pine Rd, Dallas TX 75001",
            loyalty_points=25
        )
        
        self.customer_suspended = Customer(
            customer_id=104,
            name="Diana Prince",
            email="diana@email.com",
            membership_tier="suspended",
            phone="555-0104",
            address="321 Elm St, Beverly Hills CA 90210",
            loyalty_points=75
        )
    
    def test_customer_creation(self):
        """Test customer creation with valid data"""
        customer = Customer(
            customer_id=105,
            name="Eve Wilson",
            email="eve@email.com",
            membership_tier="bronze",
            phone="555-0105",
            address="654 Maple Dr, New York NY 10002",
            loyalty_points=10
        )
        
        self.assertEqual(customer.customer_id, 105)
        self.assertEqual(customer.name, "Eve Wilson")
        self.assertEqual(customer.email.value, "eve@email.com")
        self.assertEqual(customer.membership_tier, MembershipTier.BRONZE)
        self.assertEqual(customer.phone, "555-0105")
        self.assertEqual(customer.address.street, "654 Maple Dr")
        self.assertEqual(customer.address.city, "New York")
        self.assertEqual(customer.address.state, "NY")
        self.assertEqual(customer.address.zip_code, "10002")
        self.assertEqual(customer.loyalty_points, 10)
        self.assertEqual(customer.order_history, [])
    
    def test_customer_creation_invalid_data(self):
        """Test customer creation with invalid data"""
        with self.assertRaises(ValueError):
            Customer(
                customer_id=-1,  # Invalid ID
                name="Test",
                email="test@email.com",
                membership_tier="gold",
                phone="555-0101",
                address="123 Main St, San Francisco CA 94102",
                loyalty_points=0
            )
        
        with self.assertRaises(ValueError):
            Customer(
                customer_id=106,
                name="",  # Empty name
                email="test@email.com",
                membership_tier="gold",
                phone="555-0101",
                address="123 Main St, San Francisco CA 94102",
                loyalty_points=0
            )
        
        with self.assertRaises(ValueError):
            Customer(
                customer_id=107,
                name="Test",
                email="invalid-email",  # Invalid email
                membership_tier="gold",
                phone="555-0101",
                address="123 Main St, San Francisco CA 94102",
                loyalty_points=0
            )
        
        with self.assertRaises(ValueError):
            Customer(
                customer_id=108,
                name="Test",
                email="test@email.com",
                membership_tier="gold",
                phone="555-0101",
                address="123 Main St, San Francisco CA 94102",
                loyalty_points=-10  # Negative points
            )
    
    def test_can_place_order(self):
        """Test if customer can place orders"""
        self.assertTrue(self.customer_gold.can_place_order())
        self.assertTrue(self.customer_silver.can_place_order())
        self.assertTrue(self.customer_standard.can_place_order())
        self.assertFalse(self.customer_suspended.can_place_order())
    
    def test_get_membership_discount_rate(self):
        """Test membership discount rates"""
        self.assertEqual(self.customer_gold.get_membership_discount_rate(), 0.15)
        self.assertEqual(self.customer_silver.get_membership_discount_rate(), 0.07)
        self.assertEqual(self.customer_standard.get_membership_discount_rate(), 0.0)
        self.assertEqual(self.customer_suspended.get_membership_discount_rate(), 0.0)
    
    def test_get_shipping_discount_rate(self):
        """Test shipping discount rates"""
        self.assertEqual(self.customer_gold.get_shipping_discount_rate(), 0.5)
        self.assertEqual(self.customer_silver.get_shipping_discount_rate(), 0.0)
        self.assertEqual(self.customer_standard.get_shipping_discount_rate(), 0.0)
        self.assertEqual(self.customer_suspended.get_shipping_discount_rate(), 0.0)
    
    def test_add_loyalty_points(self):
        """Test adding loyalty points"""
        initial_points = self.customer_standard.loyalty_points
        self.customer_standard.add_loyalty_points(50)
        self.assertEqual(self.customer_standard.loyalty_points, initial_points + 50)
        
        # Test with gold multiplier
        initial_points = self.customer_gold.loyalty_points
        self.customer_gold.add_loyalty_points(50)
        self.assertEqual(self.customer_gold.loyalty_points, initial_points + 100)  # 2x multiplier for gold
    
    def test_redeem_loyalty_points(self):
        """Test redeeming loyalty points"""
        initial_points = self.customer_gold.loyalty_points
        
        # Test successful redemption
        self.assertTrue(self.customer_gold.redeem_loyalty_points(50))
        self.assertEqual(self.customer_gold.loyalty_points, initial_points - 50)
        
        # Test insufficient points
        self.assertFalse(self.customer_standard.redeem_loyalty_points(100))
        self.assertEqual(self.customer_standard.loyalty_points, 25)  # Unchanged
        
        # Test invalid points
        with self.assertRaises(ValueError):
            self.customer_gold.redeem_loyalty_points(-10)
    
    def test_upgrade_membership(self):
        """Test membership upgrade"""
        # Test upgrade from standard to silver
        self.customer_standard.upgrade_membership(MembershipTier.SILVER)
        self.assertEqual(self.customer_standard.membership_tier, MembershipTier.SILVER)
        
        # Test upgrade to suspended (should fail)
        with self.assertRaises(ValueError):
            self.customer_gold.upgrade_membership(MembershipTier.SUSPENDED)
    
    def test_add_order_to_history(self):
        """Test adding order to customer history"""
        initial_count = len(self.customer_gold.order_history)
        self.customer_gold.add_order_to_history(1001)
        self.assertEqual(len(self.customer_gold.order_history), initial_count + 1)
        self.assertIn(1001, self.customer_gold.order_history)
        
        # Test invalid order ID
        with self.assertRaises(ValueError):
            self.customer_gold.add_order_to_history(-1)
    
    def test_get_customer_by_email(self):
        """Test getting customer by email"""
        # This would require a repository implementation
        # For now, just test the email value object
        self.assertEqual(self.customer_gold.email.value, "alice@email.com")
        
        # Test email validation
        with self.assertRaises(ValueError):
            Customer(
                customer_id=109,
                name="Test",
                email="invalid-email",  # Invalid email format
                membership_tier="gold",
                phone="555-0101",
                address="123 Main St, San Francisco CA 94102",
                loyalty_points=0
            )


if __name__ == '__main__':
    unittest.main()