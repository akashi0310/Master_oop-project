import unittest
import datetime
from unittest.mock import Mock, patch
from domain.models import Customer, Product, Order, OrderItem, Supplier
from domain.enums import MembershipTier, OrderStatus, ShippingMethod
from domain.value_objects import Address, Email, Money

# Import all refactored services
from services.customer_service import CustomerService
from services.order_service import OrderService
from services.product_service import ProductService
from services.supplier_service import SupplierService
from services.pricing.pricing_service import PricingService
from services.notification_service import NotificationService
from services.inventory_service import InventoryService
from services.payment_service import PaymentService
from services.shipping_service import ShippingService
from services.reporting_service import ReportingService


class TestRefactoredServices(unittest.TestCase):
    """Test suite for all refactored services"""
    
    def setUp(self):
        """Set up test data"""
        # Create test customer
        self.test_customer = Customer(
            customer_id=1,
            name="John Doe",
            email=Email("john@example.com"),
            address=Address("123 Main St", "Anytown", "CA", "12345", "USA"),
            membership_tier=MembershipTier.STANDARD
        )
        
        # Create test product
        self.test_product = Product(
            product_id=1,
            name="Test Product",
            price=Money(10.0),
            quantity_available=100,
            category="Electronics",
            weight=1.0,
            supplier_id=1
        )
        
        # Create test order
        self.test_order = Order(
            order_id=1,
            customer_id=1,
            items=[OrderItem(product_id=1, quantity=2, unit_price=Money(10.0))],
            status=OrderStatus.PENDING.value,
            created_at=datetime.datetime.now(),
            total_price=Money(20.0),
            shipping_cost=Money(5.0)
        )
        
        # Create test supplier
        self.test_supplier = Supplier(
            supplier_id=1,
            name="Test Supplier",
            email="supplier@example.com",
            reliability_score=4.0,
            phone="123-456-7890"
        )
    
    def test_customer_service(self):
        """Test CustomerService functionality"""
        service = CustomerService()
        
        # Test customer registration
        customer = service.register_customer(
            name="Jane Doe",
            email="jane@example.com",
            address=Address("456 Oak St", "Anytown", "CA", "12345", "USA")
        )
        self.assertEqual(customer.name, "Jane Doe")
        self.assertEqual(customer.email.value, "jane@example.com")
        
        # Test loyalty points
        service.add_loyalty_points(customer.customer_id, 100)
        points = service.get_loyalty_points(customer.customer_id)
        self.assertEqual(points, 100)
        
        # Test membership upgrade
        upgraded = service.upgrade_membership(customer.customer_id, MembershipTier.GOLD)
        self.assertEqual(upgraded.membership_tier, MembershipTier.GOLD)
    
    def test_order_service(self):
        """Test OrderService functionality"""
        service = OrderService()
        
        # Test order creation
        order = service.create_order(
            customer_id=1,
            order_items=[OrderItem(product_id=1, quantity=2, unit_price=Money(10.0))],
            payment_info={
                "valid": True,
                "type": "credit_card",
                "card_number": "4111111111111111",
                "amount": 100.0
            },
            products=[self.test_product],
            customer=self.test_customer,
            promotions=[],
            promo_code=None,
            shipping_method="standard",
            loyalty_points_to_use=0
        )
        self.assertEqual(order.customer_id, 1)
        self.assertEqual(len(order.items), 1)
        
        # Test order status update
        result = service.update_order_status(order.order_id, OrderStatus.PROCESSING)
        self.assertTrue(result)
        updated_order = service.get_order(order.order_id)
        self.assertEqual(updated_order.status, OrderStatus.PROCESSING)
    
    def test_product_service(self):
        """Test ProductService functionality"""
        service = ProductService()
        
        # Test product creation
        product = service.create_product(
            name="New Product",
            description="A new product",
            price=Money(15.0),
            category="Electronics"
        )
        self.assertEqual(product.name, "New Product")
        self.assertEqual(product.price.amount, 15.0)
        
        # Test product search
        results = service.search_products("Product")
        self.assertGreater(len(results), 0)
        
        # Test stock update
        service.update_stock(product.product_id, 50)
        updated = service.get_product_by_id(product.product_id)
        self.assertEqual(updated.quantity_available, 50)
    
    def test_supplier_service(self):
        """Test SupplierService functionality"""
        service = SupplierService()
        
        # Test supplier creation
        supplier = service.register_supplier(
            name="New Supplier",
            contact_email=Email("newsupplier@example.com"),
            contact_phone="987-654-3210"
        )
        self.assertEqual(supplier.name, "New Supplier")
        
        # Test supplier reliability
        service.update_reliability_score(supplier.supplier_id, 4.5)
        score = service.get_reliability_score(supplier.supplier_id)
        self.assertEqual(score, 4.5)
        
        # Test supplier status
        service.update_supplier_status(supplier.supplier_id, "Active")
        status = service.get_supplier_status(supplier.supplier_id)
        self.assertEqual(status, "Active")
    
    def test_pricing_service(self):
        """Test PricingService functionality"""
        service = PricingService()
        
        # Test price calculation
        price = service.calculate_price(
            product=self.test_product,
            quantity=2,
            customer=self.test_customer
        )
        self.assertEqual(price.amount, 20.0)
        
        # Test discount application
        discounted_price = service.apply_discount(
            price=price,
            discount_percentage=10.0
        )
        self.assertEqual(discounted_price.amount, 18.0)
        
        # Test shipping cost calculation
        shipping_cost = service.calculate_shipping_cost(
            order=self.test_order,
            shipping_method=ShippingMethod.STANDARD,
            address=self.test_customer.address
        )
        self.assertGreater(shipping_cost.amount, 0)
    
    def test_notification_service(self):
        """Test NotificationService functionality"""
        service = NotificationService()
        
        # Test order notification
        result = service.send_order_confirmation(
            customer=self.test_customer,
            order=self.test_order
        )
        self.assertTrue(result["success"])
        
        # Test marketing notification
        result = service.send_marketing_email(
            customers=[self.test_customer],
            subject="Special Offer",
            message="Get 20% off!"
        )
        self.assertTrue(result["success"])
        
        # Test notification settings
        settings = service.get_notification_settings(self.test_customer.customer_id)
        self.assertIsNotNone(settings)
    
    def test_inventory_service(self):
        """Test InventoryService functionality"""
        service = InventoryService()
        
        # Test restocking
        service.restock_product(self.test_product, 50, "Initial stock")
        self.assertEqual(self.test_product.quantity_available, 150)
        
        # Test stock deduction
        service.deduct_stock(self.test_product, 20, "Order fulfillment")
        self.assertEqual(self.test_product.quantity_available, 130)
        
        # Test low stock detection
        low_stock_products = service.get_low_stock_products([self.test_product], threshold=150)
        self.assertEqual(len(low_stock_products), 1)
        
        # Test inventory value calculation
        total_value = service.get_total_inventory_value([self.test_product])
        self.assertEqual(total_value.amount, 1300.0)  # 130 * $10
    
    def test_payment_service(self):
        """Test PaymentService functionality"""
        service = PaymentService()
        
        # Test payment validation
        is_valid = service.validate_payment_details(
            payment_method="credit_card",
            card_number="4111111111111111",
            expiry_date="12/25",
            cvv="123"
        )
        self.assertTrue(is_valid)
        
        # Test payment processing
        result = service.process_payment(
            amount=Money(20.0),
            payment_method="credit_card",
            payment_details={
                "card_number": "4111111111111111",
                "expiry_date": "12/25",
                "cvv": "123"
            }
        )
        self.assertTrue(result["success"])
        self.assertIsNotNone(result["transaction_id"])
        
        # Test refund
        refund_result = service.refund_payment(
            transaction_id=result["transaction_id"],
            amount=Money(20.0),
            reason="Customer request"
        )
        self.assertTrue(refund_result["success"])
    
    def test_shipping_service(self):
        """Test ShippingService functionality"""
        service = ShippingService()
        
        # Test shipment creation
        shipment_id = service.create_shipment(
            order_id=1,
            shipping_method=ShippingMethod.STANDARD
        )
        self.assertIsNotNone(shipment_id)
        
        # Test shipment status update
        updated = service.update_shipment_status(
            shipment_id=shipment_id,
            status="In Transit",
            location="Distribution Center"
        )
        self.assertTrue(updated)
        
        # Test shipment tracking
        shipment = service.get_shipment(shipment_id)
        self.assertEqual(shipment["status"], "In Transit")
        
        # Test shipping cost calculation
        shipping_cost = service.calculate_shipping_cost(
            order=self.test_order,
            shipping_method=ShippingMethod.STANDARD,
            address=self.test_customer.address
        )
        self.assertGreater(shipping_cost.amount, 0)
    
    def test_reporting_service(self):
        """Test ReportingService functionality"""
        service = ReportingService()
        service.set_data(
            customers=[self.test_customer],
            products=[self.test_product],
            orders=[self.test_order]
        )
        
        # Test sales summary
        sales_summary = service.get_sales_summary()
        self.assertEqual(sales_summary["total_orders"], 1)
        self.assertEqual(sales_summary["total_sales"].amount, 20.0)
        
        # Test product performance
        product_performance = service.get_product_performance()
        self.assertIn(1, product_performance)
        self.assertEqual(product_performance[1]["sold"], 2)
        
        # Test customer summary
        customer_summary = service.get_customer_summary()
        self.assertIn(1, customer_summary)
        self.assertEqual(customer_summary[1]["total_orders"], 1)
        
        # Test low stock products
        low_stock = service.get_low_stock_products(threshold=150)
        self.assertEqual(len(low_stock), 1)
        
        # Test customer segmentation
        segmentation = service.get_customer_segmentation()
        self.assertIn("New", segmentation)


if __name__ == "__main__":
    unittest.main()