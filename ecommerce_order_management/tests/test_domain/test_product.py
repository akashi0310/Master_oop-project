import unittest
from ecommerce_order_management.domain.models.product import Product, ProductId, SupplierId
from ecommerce_order_management.domain.value_objects.money import Money

class TestProduct(unittest.TestCase):
    def test_product_creation_valid(self):
        product = Product(
            product_id=ProductId("P001"),
            name="Laptop",
            price=Money(1200.00),
            quantity_available=10,
            category="Electronics",
            weight=2.5,
            supplier_id=SupplierId("S001")
        )
        self.assertEqual(product.product_id, "P001")
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.price, Money(1200.00))
        self.assertEqual(product.quantity_available, 10)
        self.assertEqual(product.category, "Electronics")
        self.assertEqual(product.weight, 2.5)
        self.assertEqual(product.supplier_id, "S001")
        self.assertTrue(product.discount_eligible)

    def test_product_creation_invalid_empty_product_id(self):
        with self.assertRaisesRegex(ValueError, "Product ID must be a non-empty string."):
            Product(
                product_id=ProductId(""),
                name="Laptop",
                price=Money(1200.00),
                quantity_available=10,
                category="Electronics",
                weight=2.5,
                supplier_id=SupplierId("S001")
            )

    def test_product_creation_invalid_negative_price(self):
        with self.assertRaisesRegex(ValueError, "Price must be a Money object with a positive amount."):
            Product(
                product_id=ProductId("P001"),
                name="Laptop",
                price=Money(-100.00),
                quantity_available=10,
                category="Electronics",
                weight=2.5,
                supplier_id=SupplierId("S001")
            )

    def test_product_creation_invalid_zero_quantity(self):
        with self.assertRaisesRegex(ValueError, "Quantity available must be a non-negative integer."):
            Product(
                product_id=ProductId("P001"),
                name="Laptop",
                price=Money(1200.00),
                quantity_available=-5,
                category="Electronics",
                weight=2.5,
                supplier_id=SupplierId("S001")
            )

    def test_product_creation_invalid_empty_category(self):
        with self.assertRaisesRegex(ValueError, "Category must be a non-empty string."):
            Product(
                product_id=ProductId("P001"),
                name="Laptop",
                price=Money(1200.00),
                quantity_available=10,
                category="",
                weight=2.5,
                supplier_id=SupplierId("S001")
            )

    def test_product_creation_invalid_zero_weight(self):
        with self.assertRaisesRegex(ValueError, "Weight must be a positive number."):
            Product(
                product_id=ProductId("P001"),
                name="Laptop",
                price=Money(1200.00),
                quantity_available=10,
                category="Electronics",
                weight=0,
                supplier_id=SupplierId("S001")
            )

    def test_product_creation_invalid_empty_supplier_id(self):
        with self.assertRaisesRegex(ValueError, "Supplier ID must be a non-empty string."):
            Product(
                product_id=ProductId("P001"),
                name="Laptop",
                price=Money(1200.00),
                quantity_available=10,
                category="Electronics",
                weight=2.5,
                supplier_id=SupplierId("")
            )

if __name__ == '__main__':
    unittest.main()