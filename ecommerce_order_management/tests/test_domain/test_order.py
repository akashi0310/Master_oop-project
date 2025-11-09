import unittest
import datetime
from ecommerce_order_management.domain.models.order import Order, OrderId
from ecommerce_order_management.domain.models.order_item import OrderItem, ProductId
from ecommerce_order_management.domain.models.customer import CustomerId
from ecommerce_order_management.domain.value_objects.money import Money

class TestOrder(unittest.TestCase):
    def setUp(self):
        self.sample_order_item = OrderItem(
            product_id=ProductId("P001"),
            quantity=2,
            unit_price=Money(50.00)
        )
        self.sample_order_items = [self.sample_order_item]

    def test_order_creation_valid(self):
        order = Order(
            order_id=OrderId("ORD001"),
            customer_id=CustomerId("C001"),
            items=self.sample_order_items,
            status="pending",
            created_at=datetime.datetime.now(),
            total_price=Money(100.00),
            shipping_cost=Money(10.00)
        )
        self.assertEqual(order.order_id, "ORD001")
        self.assertEqual(order.customer_id, "C001")
        self.assertEqual(order.items, self.sample_order_items)
        self.assertEqual(order.status, "pending")
        self.assertIsInstance(order.created_at, datetime.datetime)
        self.assertEqual(order.total_price, Money(100.00))
        self.assertEqual(order.shipping_cost, Money(10.00))
        self.assertIsNone(order.tracking_number)
        self.assertIsNone(order.payment_method)

    def test_order_creation_invalid_empty_order_id(self):
        with self.assertRaisesRegex(ValueError, "Order ID must be a non-empty string."):
            Order(
                order_id=OrderId(""),
                customer_id=CustomerId("C001"),
                items=self.sample_order_items,
                status="pending",
                created_at=datetime.datetime.now(),
                total_price=Money(100.00),
                shipping_cost=Money(10.00)
            )

    def test_order_creation_invalid_empty_customer_id(self):
        with self.assertRaisesRegex(ValueError, "Customer ID must be a non-empty string."):
            Order(
                order_id=OrderId("ORD001"),
                customer_id=CustomerId(""),
                items=self.sample_order_items,
                status="pending",
                created_at=datetime.datetime.now(),
                total_price=Money(100.00),
                shipping_cost=Money(10.00)
            )

    def test_order_creation_invalid_items_type(self):
        with self.assertRaisesRegex(ValueError, "Items must be a list of OrderItem objects."):
            Order(
                order_id=OrderId("ORD001"),
                customer_id=CustomerId("C001"),
                items=["not an order item"],
                status="pending",
                created_at=datetime.datetime.now(),
                total_price=Money(100.00),
                shipping_cost=Money(10.00)
            )

    def test_order_creation_invalid_status(self):
        with self.assertRaisesRegex(ValueError, "Invalid order status."):
            Order(
                order_id=OrderId("ORD001"),
                customer_id=CustomerId("C001"),
                items=self.sample_order_items,
                status="invalid_status",
                created_at=datetime.datetime.now(),
                total_price=Money(100.00),
                shipping_cost=Money(10.00)
            )

    def test_order_creation_invalid_total_price_negative(self):
        with self.assertRaisesRegex(ValueError, "Total price must be a Money object with a non-negative amount."):
            Order(
                order_id=OrderId("ORD001"),
                customer_id=CustomerId("C001"),
                items=self.sample_order_items,
                status="pending",
                created_at=datetime.datetime.now(),
                total_price=Money(-10.00),
                shipping_cost=Money(10.00)
            )

    def test_order_creation_invalid_shipping_cost_negative(self):
        with self.assertRaisesRegex(ValueError, "Shipping cost must be a Money object with a non-negative amount."):
            Order(
                order_id=OrderId("ORD001"),
                customer_id=CustomerId("C001"),
                items=self.sample_order_items,
                status="pending",
                created_at=datetime.datetime.now(),
                total_price=Money(100.00),
                shipping_cost=Money(-5.00)
            )

if __name__ == '__main__':
    unittest.main()