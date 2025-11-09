import unittest
from ecommerce_order_management.domain.models.order_item import OrderItem, ProductId
from ecommerce_order_management.domain.value_objects.money import Money

class TestOrderItem(unittest.TestCase):
    def test_order_item_creation_valid(self):
        item = OrderItem(
            product_id=ProductId("P001"),
            quantity=2,
            unit_price=Money(50.00)
        )
        self.assertEqual(item.product_id, "P001")
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.unit_price, Money(50.00))
        self.assertEqual(item.discount_applied, Money(0.0))

    def test_order_item_creation_invalid_empty_product_id(self):
        with self.assertRaisesRegex(ValueError, "Product ID must be a non-empty string."):
            OrderItem(
                product_id=ProductId(""),
                quantity=2,
                unit_price=Money(50.00)
            )

    def test_order_item_creation_invalid_zero_quantity(self):
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            OrderItem(
                product_id=ProductId("P001"),
                quantity=0,
                unit_price=Money(50.00)
            )

    def test_order_item_creation_invalid_negative_quantity(self):
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            OrderItem(
                product_id=ProductId("P001"),
                quantity=-1,
                unit_price=Money(50.00)
            )

    def test_order_item_creation_invalid_zero_unit_price(self):
        with self.assertRaisesRegex(ValueError, "Unit price must be a Money object with a positive amount."):
            OrderItem(
                product_id=ProductId("P001"),
                quantity=2,
                unit_price=Money(0.0)
            )

    def test_order_item_creation_invalid_negative_unit_price(self):
        with self.assertRaisesRegex(ValueError, "Unit price must be a Money object with a positive amount."):
            OrderItem(
                product_id=ProductId("P001"),
                quantity=2,
                unit_price=Money(-10.0)
            )

    def test_order_item_creation_invalid_unit_price_type(self):
        with self.assertRaisesRegex(ValueError, "Unit price must be a Money object with a positive amount."):
            OrderItem(
                product_id=ProductId("P001"),
                quantity=2,
                unit_price=10.0 # Should be Money object
            )

if __name__ == '__main__':
    unittest.main()