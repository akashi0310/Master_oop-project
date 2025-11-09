import unittest
from domain.value_objects.address import Address

class TestAddress(unittest.TestCase):
    def test_address_creation_valid(self):
        address = Address(
            street="123 Main St",
            city="Anytown",
            state="CA",
            zip_code="90210",
            country="USA"
        )
        self.assertEqual(address.street, "123 Main St")
        self.assertEqual(address.city, "Anytown")
        self.assertEqual(address.state, "CA")
        self.assertEqual(address.zip_code, "90210")
        self.assertEqual(address.country, "USA")

    def test_address_creation_invalid_empty_street(self):
        with self.assertRaisesRegex(ValueError, "All address components must be non-empty strings."):
            Address(street="", city="Anytown", state="CA", zip_code="90210", country="USA")

    def test_address_creation_invalid_non_string_city(self):
        with self.assertRaisesRegex(ValueError, "All address components must be non-empty strings."):
            Address(street="123 Main St", city="", state="CA", zip_code="90210", country="USA")

    def test_address_equality(self):
        address1 = Address("123 Main St", "Anytown", "CA", "90210", "USA")
        address2 = Address("123 Main St", "Anytown", "CA", "90210", "USA")
        address3 = Address("456 Oak Ave", "Otherville", "NY", "10001", "USA")
        self.assertEqual(address1, address2)
        self.assertNotEqual(address1, address3)

if __name__ == '__main__':
    unittest.main()