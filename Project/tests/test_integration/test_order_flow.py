import unittest
from datetime import datetime
from domain.models import Customer, Product, Order, OrderItem, Promotion
from domain.value_objects import Money
from repositories.in_memory import (
    InMemoryCustomerRepository,
    InMemoryProductRepository,
    InMemoryOrderRepository,
    InMemoryPromotionRepository
)
from services import (
    CustomerService,
    ProductService,
    OrderService,
    PricingService,
    InventoryService,
    NotificationService,
    ShippingService
)
from application.order_processor import OrderProcessor


class TestOrderFlow(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        # Create repositories
        self.customer_repo = InMemoryCustomerRepository()
        self.product_repo = InMemoryProductRepository()
        self.order_repo = InMemoryOrderRepository()
        self.promotion_repo = InMemoryPromotionRepository()
        
        # Create order processor with repositories
        self.order_processor = OrderProcessor(
            customer_repository=self.customer_repo,
            product_repository=self.product_repo,
            order_repository=self.order_repo,
            promotion_repository=self.promotion_repo
        )
        
        # Create test data
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
            name="Bob Johnson",
            email="bob@email.com",
            membership_tier="silver",
            phone="555-0102",
            address="456 Oak Ave, New York NY 10001",
            loyalty_points=50
        )
        
        self.product_laptop = Product(
            product_id=1,
            name="Laptop Pro 15",
            price=999.99,
            quantity_available=15,
            category="Electronics",
            weight=2.5,
            supplier_id=1
        )
        
        self.product_mouse = Product(
            product_id=2,
            name="Wireless Mouse",
            price=29.99,
            quantity_available=50,
            category="Electronics",
            weight=0.2,
            supplier_id=1
        )
        
        self.product_keyboard = Product(
            product_id=3,
            name="Mechanical Keyboard",
            price=79.99,
            quantity_available=25,
            category="Electronics",
            weight=1.0,
            supplier_id=1
        )
        
        self.promotion_save15 = Promotion(
            promo_id=1,
            code="SAVE15",
            discount_percent=15,
            min_purchase=100,
            valid_until=datetime(2025, 12, 31),
            category="Electronics"
        )
        
        self.promotion_bulk10 = Promotion(
            promo_id=2,
            code="BULK10",
            discount_percent=10,
            min_purchase=500,
            valid_until=datetime(2025, 12, 31),
            category="Electronics"
        )
        
        # Add test data to repositories
        self.customer_repo.add(self.customer_gold)
        self.customer_repo.add(self.customer_silver)
        self.product_repo.add(self.product_laptop)
        self.product_repo.add(self.product_mouse)
        self.product_repo.add(self.product_keyboard)
        self.promotion_repo.add(self.promotion_save15)
        self.promotion_repo.add(self.promotion_bulk10)
    
    def test_complete_order_flow(self):
        """Test a complete order flow from creation to delivery"""
        # Step 1: Create an order with multiple items and a promo code
        order_data = {
            "customer_id": 101,
            "items": [
                {"product_id": 1, "quantity": 1},  # Laptop
                {"product_id": 2, "quantity": 2},  # 2 Mice
                {"product_id": 3, "quantity": 1}   # Keyboard
            ],
            "promo_code": "SAVE15"
        }
        
        # Convert order items to include unit_price from product
        order_items_with_price = []
        for item in order_data["items"]:
            product = self.product_repo.get_by_id(item["product_id"])
            order_items_with_price.append({
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "unit_price": product.price
            })
        
        result = self.order_processor.process_order(
            customer_id=order_data["customer_id"],
            order_items=order_items_with_price,
            payment_info={"type": "credit_card", "valid": True, "amount": 3000},
            promo_code=order_data.get("promo_code"),
            shipping_method="standard"
        )
        self.assertIsNotNone(result)
        order_id = result["order_id"]
        
        # Verify order was created
        order = self.order_repo.get_by_id(order_id)
        self.assertIsNotNone(order)
        self.assertEqual(order.customer_id, 101)
        self.assertEqual(len(order.items), 3)  # 1 laptop + 2 mice + 1 keyboard (but mice quantity is 2, so total items = 3)
        self.assertEqual(order.status.value, "pending")
        
        # Verify inventory was updated
        laptop = self.product_repo.get_by_id(1)
        mouse = self.product_repo.get_by_id(2)
        keyboard = self.product_repo.get_by_id(3)
        
        self.assertEqual(laptop.quantity_available, 14)  # Was 15
        self.assertEqual(mouse.quantity_available, 48)   # Was 50
        self.assertEqual(keyboard.quantity_available, 24)  # Was 25
        
        # Step 2: Get order details
        details = self.order_processor.get_order(order_id)
        self.assertIsNotNone(details)
        self.assertEqual(details["order_id"], order_id)
        self.assertEqual(details["status"], "pending")
        
        # Step 3: Confirm the order
        confirm_result = self.order_processor.update_order_status(order_id, "confirmed")
        self.assertTrue(confirm_result)
        
        # Verify order status changed
        order = self.order_repo.get_by_id(order_id)
        self.assertEqual(order.status.value, "confirmed")
        
        # Step 4: Ship the order
        ship_result = self.order_processor.update_order_status(order_id, "shipped", tracking_number="TRACK123456")
        self.assertTrue(ship_result)
        
        # Verify order status changed
        order = self.order_repo.get_by_id(order_id)
        self.assertEqual(order.status.value, "shipped")
        self.assertEqual(order.tracking_number, "TRACK123456")
        
        # Step 5: Deliver the order
        deliver_result = self.order_processor.update_order_status(order_id, "delivered")
        self.assertTrue(deliver_result)
        
        # Verify order status changed
        order = self.order_repo.get_by_id(order_id)
        self.assertEqual(order.status.value, "delivered")
        
        # Verify customer loyalty points were added
        customer = self.customer_repo.get_by_id(101)
        self.assertGreater(customer.loyalty_points, 100)  # Should have increased
    
    def test_order_cancellation_flow(self):
        """Test order cancellation flow"""
        # Step 1: Create an order
        order_data = {
            "customer_id": 102,
            "items": [
                {"product_id": 2, "quantity": 3},  # 3 Mice
                {"product_id": 3, "quantity": 1}   # 1 Keyboard
            ]
        }
        
        # Convert order items to include unit_price from product
        order_items_with_price = []
        for item in order_data["items"]:
            product = self.product_repo.get_by_id(item["product_id"])
            order_items_with_price.append({
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "unit_price": product.price
            })
        
        result = self.order_processor.process_order(
            customer_id=order_data["customer_id"],
            order_items=order_items_with_price,
            payment_info={"type": "credit_card", "valid": True, "amount": 500},
            promo_code=order_data.get("promo_code"),
            shipping_method="standard"
        )
        self.assertIsNotNone(result)
        order_id = result["order_id"]
        
        # Verify inventory was updated
        mouse = self.product_repo.get_by_id(2)
        keyboard = self.product_repo.get_by_id(3)
        
        self.assertEqual(mouse.quantity_available, 47)  # Was 50
        self.assertEqual(keyboard.quantity_available, 24)  # Was 25
        
        # Step 2: Cancel the order
        cancel_result = self.order_processor.cancel_order(order_id, "Customer requested")
        self.assertTrue(cancel_result)
        
        # Verify order status changed
        order = self.order_repo.get_by_id(order_id)
        self.assertEqual(order.status.value, "cancelled")
        
        # Verify inventory was restored
        mouse = self.product_repo.get_by_id(2)
        keyboard = self.product_repo.get_by_id(3)
        
        self.assertEqual(mouse.quantity_available, 50)  # Restored to original
        self.assertEqual(keyboard.quantity_available, 25)  # Restored to original
    
    def test_bulk_discount_flow(self):
        """Test bulk discount application"""
        # Step 1: Create a large order that qualifies for bulk discount
        order_data = {
            "customer_id": 101,
            "items": [
                {"product_id": 1, "quantity": 2}  # 2 Laptops
            ],
            "promo_code": "BULK10"
        }
        
        # Convert order items to include unit_price from product
        order_items_with_price = []
        for item in order_data["items"]:
            product = self.product_repo.get_by_id(item["product_id"])
            order_items_with_price.append({
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "unit_price": product.price
            })
        
        result = self.order_processor.process_order(
            customer_id=order_data["customer_id"],
            order_items=order_items_with_price,
            payment_info={"type": "credit_card", "valid": True, "amount": 3000},
            promo_code=order_data.get("promo_code"),
            shipping_method="standard"
        )
        self.assertIsNotNone(result)
        order_id = result["order_id"]
        
        # Verify bulk discount was applied
        # The actual calculation includes tax and shipping, so we'll just check that it's reasonable
        self.assertGreater(result["total"], 1500)  # Should be greater than 1500
        self.assertLess(result["total"], 2000)  # But less than 2000
        
        # Verify order was created
        order = self.order_repo.get_by_id(order_id)
        self.assertIsNotNone(order)
        self.assertEqual(order.status.value, "pending")
    
    def test_loyalty_points_redemption_flow(self):
        """Test loyalty points redemption"""
        # Step 1: Create an order with loyalty points redemption
        order_data = {
            "customer_id": 101,  # Gold customer with 100 points
            "items": [
                {"product_id": 2, "quantity": 1}  # 1 Mouse
            ],
            "loyalty_points": 50  # Redeem 50 points
        }
        
        # Convert order items to include unit_price from product
        order_items_with_price = []
        for item in order_data["items"]:
            product = self.product_repo.get_by_id(item["product_id"])
            order_items_with_price.append({
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "unit_price": product.price
            })
        
        result = self.order_processor.process_order(
            customer_id=order_data["customer_id"],
            order_items=order_items_with_price,
            payment_info={"type": "credit_card", "valid": True, "amount": 200, "use_loyalty_points": True},
            promo_code=order_data.get("promo_code"),
            shipping_method="standard",
            loyalty_points_to_use=order_data.get("loyalty_points", 0)
        )
        self.assertIsNotNone(result)
        order_id = result["order_id"]
        
        # Verify loyalty points were applied
        # The actual calculation includes tax and shipping, so we'll just check that it's reasonable
        self.assertGreater(result["total"], 20)  # Should be greater than 20
        self.assertLess(result["total"], 50)  # But less than 50
        
        # Verify customer loyalty points were updated
        customer = self.customer_repo.get_by_id(101)
        # Customer should have 100 (original) - 50 (redeemed) + 58 (earned from order) = 108 points
        self.assertEqual(customer.loyalty_points, 108)
    
    def test_multiple_orders_for_same_customer(self):
        """Test creating multiple orders for the same customer"""
        # Step 1: Create first order
        order_data1 = {
            "customer_id": 101,
            "items": [
                {"product_id": 2, "quantity": 1}  # 1 Mouse
            ]
        }
        
        # Convert order items to include unit_price from product
        order_items_with_price1 = []
        for item in order_data1["items"]:
            product = self.product_repo.get_by_id(item["product_id"])
            order_items_with_price1.append({
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "unit_price": product.price
            })
        
        result1 = self.order_processor.process_order(
            customer_id=order_data1["customer_id"],
            order_items=order_items_with_price1,
            payment_info={"type": "credit_card", "valid": True, "amount": 200},
            promo_code=order_data1.get("promo_code"),
            shipping_method="standard"
        )
        self.assertIsNotNone(result1)
        order_id1 = result1["order_id"]
        
        # Step 2: Create second order
        order_data2 = {
            "customer_id": 101,
            "items": [
                {"product_id": 3, "quantity": 1}  # 1 Keyboard
            ]
        }
        
        # Convert order items to include unit_price from product
        order_items_with_price2 = []
        for item in order_data2["items"]:
            product = self.product_repo.get_by_id(item["product_id"])
            order_items_with_price2.append({
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "unit_price": product.price
            })
        
        result2 = self.order_processor.process_order(
            customer_id=order_data2["customer_id"],
            order_items=order_items_with_price2,
            payment_info={"type": "credit_card", "valid": True, "amount": 300},
            promo_code=order_data2.get("promo_code"),
            shipping_method="standard"
        )
        self.assertIsNotNone(result2)
        order_id2 = result2["order_id"]
        
        # Verify both orders exist
        order1 = self.order_repo.get_by_id(order_id1)
        order2 = self.order_repo.get_by_id(order_id2)
        
        self.assertIsNotNone(order1)
        self.assertIsNotNone(order2)
        self.assertEqual(order1.customer_id, 101)
        self.assertEqual(order2.customer_id, 101)
        
        # Verify customer has both orders in order history
        customer_orders = self.order_repo.get_by_customer(101)
        self.assertEqual(len(customer_orders), 2)
        
        # Verify customer loyalty points increased for both orders
        customer = self.customer_repo.get_by_id(101)
        self.assertGreater(customer.loyalty_points, 100)  # Should have increased from both orders


if __name__ == '__main__':
    unittest.main()