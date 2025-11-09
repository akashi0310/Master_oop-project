import unittest
from typing import List
from ecommerce_order_management.domain.models.customer import Customer, CustomerId
from ecommerce_order_management.domain.value_objects.address import Address
from ecommerce_order_management.domain.value_objects.email import Email

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.sample_address = Address(
            street="123 Main St",
            city="Anytown",
            state="CA",
            zip_code="90210",
            country="USA"
        )
        self.sample_email = Email("test@example.com")

    def test_customer_creation_valid(self):
        customer = Customer(
            customer_id=CustomerId("C001"),
            name="John Doe",
            email=self.sample_email,
            membership_tier="standard",
            phone="555-1234",
            address=self.sample_address,
            loyalty_points=100
        )
        self.assertEqual(customer.customer_id, "C001")
        self.assertEqual(customer.name, "John Doe")
        self.assertEqual(customer.email, self.sample_email)
        self.assertEqual(customer.membership_tier, "standard")
        self.assertEqual(customer.phone, "555-1234")
        self.assertEqual(customer.address, self.sample_address)
        self.assertEqual(customer.loyalty_points, 100)
        self.assertEqual(customer.order_history, [])

    def test_customer_creation_invalid_empty_customer_id(self):
        with self.assertRaisesRegex(ValueError, "Customer ID must be a non-empty string."):
            Customer(
                customer_id=CustomerId(""),
                name="John Doe",
                email=self.sample_email,
                membership_tier="standard",
                phone="555-1234",
                address=self.sample_address,
                loyalty_points=100
            )

    def test_customer_creation_invalid_empty_name(self):
        with self.assertRaisesRegex(ValueError, "Customer name must be a non-empty string."):
            Customer(
                customer_id=CustomerId("C001"),
                name="",
                email=self.sample_email,
                membership_tier="standard",
                phone="555-1234",
                address=self.sample_address,
                loyalty_points=100
            )

    def test_customer_creation_invalid_email_object(self):
        with self.assertRaisesRegex(ValueError, "Email must be an Email object."):
            Customer(
                customer_id=CustomerId("C001"),
                name="John Doe",
                email="invalid-email", # Should be an Email object
                membership_tier="standard",
                phone="555-1234",
                address=self.sample_address,
                loyalty_points=100
            )

    def test_customer_creation_invalid_membership_tier(self):
        with self.assertRaisesRegex(ValueError, "Invalid membership tier."):
            Customer(
                customer_id=CustomerId("C001"),
                name="John Doe",
                email=self.sample_email,
                membership_tier="premium", # Invalid tier
                phone="555-1234",
                address=self.sample_address,
                loyalty_points=100
            )

    def test_customer_creation_invalid_empty_phone(self):
        with self.assertRaisesRegex(ValueError, "Phone number must be a non-empty string."):
            Customer(
                customer_id=CustomerId("C001"),
                name="John Doe",
                email=self.sample_email,
                membership_tier="standard",
                phone="",
                address=self.sample_address,
                loyalty_points=100
            )

    def test_customer_creation_invalid_address_object(self):
        with self.assertRaisesRegex(ValueError, "Address must be an Address object."):
            Customer(
                customer_id=CustomerId("C001"),
                name="John Doe",
                email=self.sample_email,
                membership_tier="standard",
                phone="555-1234",
                address="123 Main St", # Should be an Address object
                loyalty_points=100
            )

    def test_customer_creation_invalid_negative_loyalty_points(self):
        with self.assertRaisesRegex(ValueError, "Loyalty points must be a non-negative integer."):
            Customer(
                customer_id=CustomerId("C001"),
                name="John Doe",
                email=self.sample_email,
                membership_tier="standard",
                phone="555-1234",
                address=self.sample_address,
                loyalty_points=-10
            )

if __name__ == '__main__':
    unittest.main()