import unittest
from datetime import datetime, timedelta
from domain.models.order import Order
from domain.models.order_item import OrderItem
from domain.value_objects.money import Money
from domain.enums.order_status import OrderStatus
from services.order_status_manager import OrderStatusManager
from services.order_tracking_manager import OrderTrackingManager
from services.order_calculations_service import OrderCalculationsService


class TestOrderRefactored(unittest.TestCase):
    """Test cases for the refactored Order class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.items = [
            OrderItem(product_id=1, quantity=2, unit_price=Money(10.0)),
            OrderItem(product_id=2, quantity=1, unit_price=Money(20.0))
        ]
        self.status_manager = OrderStatusManager(OrderStatus.PENDING)
        self.tracking_manager = OrderTrackingManager()
        self.calculations_service = OrderCalculationsService(
            type('OrderItemsProvider', (object,), {
                'get_items': lambda: self.items
            })
        )
    
    def test_order_creation(self):
        """Test creating a valid order"""
        order = Order(
            order_id=1,
            customer_id=101,
            items=self.items,
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
            total_price=Money(40.0),
            shipping_cost=Money(5.0),
            status_manager=self.status_manager,
            tracking_manager=self.tracking_manager,
            calculations_service=self.calculations_service
        )
        
        self.assertEqual(order.order_id, 1)
        self.assertEqual(order.customer_id, 101)
        self.assertEqual(len(order.items), 2)
        self.assertEqual(order._status_manager.status, OrderStatus.PENDING)
        self.assertEqual(order.total_price, Money(40.0))
        self.assertEqual(order.shipping_cost, Money(5.0))
    
    def test_order_validation(self):
        """Test order validation"""
        with self.assertRaises(ValueError):
            Order(
                order_id=0,
                customer_id=101,
                items=self.items,
                status=OrderStatus.PENDING,
                created_at=datetime.now(),
                total_price=Money(40.0),
                shipping_cost=Money(5.0)
            )
        
        with self.assertRaises(ValueError):
            Order(
                order_id=1,
                customer_id=0,
                items=self.items,
                status=OrderStatus.PENDING,
                created_at=datetime.now(),
                total_price=Money(40.0),
                shipping_cost=Money(5.0)
            )
        
        with self.assertRaises(ValueError):
            Order(
                order_id=1,
                customer_id=101,
                items=[],
                status=OrderStatus.PENDING,
                created_at=datetime.now(),
                total_price=Money(40.0),
                shipping_cost=Money(5.0)
            )
        
        with self.assertRaises(ValueError):
            Order(
                order_id=1,
                customer_id=101,
                items=self.items,
                status="invalid",
                created_at=datetime.now(),
                total_price=Money(40.0),
                shipping_cost=Money(5.0)
            )
    
    def test_status_operations(self):
        """Test order status operations"""
        order = Order(
            order_id=1,
            customer_id=101,
            items=self.items,
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
            total_price=Money(40.0),
            shipping_cost=Money(5.0),
            status_manager=self.status_manager,
            tracking_manager=self.tracking_manager,
            calculations_service=self.calculations_service
        )
        
        # Test status update
        order.update_status(OrderStatus.PROCESSING)
        self.assertEqual(order._status_manager.status, OrderStatus.PROCESSING)
        
        # Test cancellation
        order.cancel()
        self.assertEqual(order._status_manager.status, OrderStatus.CANCELLED)
        self.assertTrue(order.is_cancelled())
        
        # Test that final status can't be changed
        with self.assertRaises(ValueError):
            order.update_status(OrderStatus.SHIPPED)
    
    def test_tracking_operations(self):
        """Test order tracking operations"""
        order = Order(
            order_id=1,
            customer_id=101,
            items=self.items,
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
            total_price=Money(40.0),
            shipping_cost=Money(5.0),
            status_manager=self.status_manager,
            tracking_manager=self.tracking_manager,
            calculations_service=self.calculations_service
        )
        
        # Test tracking number
        order.add_tracking_number("TRACK123")
        self.assertEqual(order.tracking_number, "TRACK123")
        
        # Test payment method
        order.set_payment_method("Credit Card")
        self.assertEqual(order.payment_method, "Credit Card")
        
        # Test validation
        with self.assertRaises(ValueError):
            order.add_tracking_number("")
        
        with self.assertRaises(ValueError):
            order.set_payment_method("")
    
    def test_calculation_operations(self):
        """Test order calculation operations"""
        order = Order(
            order_id=1,
            customer_id=101,
            items=self.items,
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
            total_price=Money(40.0),
            shipping_cost=Money(5.0),
            status_manager=self.status_manager,
            tracking_manager=self.tracking_manager,
            calculations_service=self.calculations_service
        )
        
        # Test subtotal calculation
        expected_subtotal = Money(40.0)  # 2 * $10 + 1 * $20
        self.assertEqual(order.get_subtotal(), expected_subtotal)
        
        # Test days since creation
        created_date = datetime.now() - timedelta(days=5)
        order = Order(
            order_id=1,
            customer_id=101,
            items=self.items,
            status=OrderStatus.PENDING,
            created_at=created_date,
            total_price=Money(40.0),
            shipping_cost=Money(5.0),
            status_manager=self.status_manager,
            tracking_manager=self.tracking_manager,
            calculations_service=self.calculations_service
        )
        self.assertEqual(order.get_days_since_creation(), 5)
    
    def test_interface_compliance(self):
        """Test that Order complies with all interfaces"""
        order = Order(
            order_id=1,
            customer_id=101,
            items=self.items,
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
            total_price=Money(40.0),
            shipping_cost=Money(5.0),
            status_manager=self.status_manager,
            tracking_manager=self.tracking_manager,
            calculations_service=self.calculations_service
        )
        
        # Test OrderInfo interface
        self.assertEqual(order.order_id, 1)
        self.assertEqual(order.customer_id, 101)
        self.assertEqual(order.items, self.items)
        # Remove seconds for comparison
        self.assertEqual(order.created_at.replace(microsecond=0), datetime.now().replace(microsecond=0))
        self.assertEqual(order.total_price, Money(40.0))
        self.assertEqual(order.shipping_cost, Money(5.0))
        
        # Test OrderStatusOperations interface
        self.assertFalse(order.is_shipped())
        self.assertFalse(order.is_delivered())
        self.assertFalse(order.is_cancelled())
        self.assertTrue(order.can_be_cancelled())
        
        # Test OrderTrackingOperations interface
        self.assertIsNone(order.tracking_number)
        self.assertIsNone(order.payment_method)
        
        # Test OrderCalculationOperations interface
        self.assertEqual(order.get_subtotal(), Money(40.0))


if __name__ == '__main__':
    unittest.main()