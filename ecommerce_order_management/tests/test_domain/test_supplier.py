import unittest
from ecommerce_order_management.domain.models.supplier import Supplier, SupplierId
from ecommerce_order_management.domain.value_objects.email import Email

class TestSupplier(unittest.TestCase):
    def setUp(self):
        self.sample_email = Email("supplier@example.com")

    def test_supplier_creation_valid(self):
        supplier = Supplier(
            supplier_id=SupplierId("S001"),
            name="Tech Distributors",
            email=self.sample_email,
            reliability_score=0.95
        )
        self.assertEqual(supplier.supplier_id, "S001")
        self.assertEqual(supplier.name, "Tech Distributors")
        self.assertEqual(supplier.email, self.sample_email)
        self.assertEqual(supplier.reliability_score, 0.95)

    def test_supplier_creation_invalid_empty_supplier_id(self):
        with self.assertRaisesRegex(ValueError, "Supplier ID must be a non-empty string."):
            Supplier(
                supplier_id=SupplierId(""),
                name="Tech Distributors",
                email=self.sample_email,
                reliability_score=0.95
            )

    def test_supplier_creation_invalid_empty_name(self):
        with self.assertRaisesRegex(ValueError, "Supplier name must be a non-empty string."):
            Supplier(
                supplier_id=SupplierId("S001"),
                name="",
                email=self.sample_email,
                reliability_score=0.95
            )

    def test_supplier_creation_invalid_email_object(self):
        with self.assertRaisesRegex(ValueError, "Email must be an Email object."):
            Supplier(
                supplier_id=SupplierId("S001"),
                name="Tech Distributors",
                email="invalid-email", # Should be an Email object
                reliability_score=0.95
            )

    def test_supplier_creation_invalid_reliability_score_too_low(self):
        with self.assertRaisesRegex(ValueError, "Reliability score must be between 0 and 1."):
            Supplier(
                supplier_id=SupplierId("S001"),
                name="Tech Distributors",
                email=self.sample_email,
                reliability_score=-0.1
            )

    def test_supplier_creation_invalid_reliability_score_too_high(self):
        with self.assertRaisesRegex(ValueError, "Reliability score must be between 0 and 1."):
            Supplier(
                supplier_id=SupplierId("S001"),
                name="Tech Distributors",
                email=self.sample_email,
                reliability_score=1.1
            )

if __name__ == '__main__':
    unittest.main()