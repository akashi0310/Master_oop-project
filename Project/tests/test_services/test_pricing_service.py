import unittest
from datetime import datetime, timedelta
from domain.models import Customer, OrderItem, Product, Promotion
from domain.value_objects import Money
from domain.enums import ShippingMethod, MembershipTier
from services.pricing.pricing_service import PricingService
from services.pricing.strategies import (
    MembershipDiscountStrategy,
    PromotionalDiscountStrategy,
    BulkDiscountStrategy,
    LoyaltyDiscountStrategy
)


class TestPricingService(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.pricing_service = PricingService()
        
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
        
        self.order_items = [
            OrderItem(product_id=1, quantity=1, unit_price=999.99),
            OrderItem(product_id=2, quantity=2, unit_price=29.99),
            OrderItem(product_id=3, quantity=5, unit_price=79.99)
        ]
        
        self.products = [
            Product(product_id=1, name="Laptop", price=999.99, quantity_available=15, category="Electronics", weight=2.5, supplier_id=1),
            Product(product_id=2, name="Mouse", price=29.99, quantity_available=50, category="Electronics", weight=0.2, supplier_id=2),
            Product(product_id=3, name="Keyboard", price=79.99, quantity_available=30, category="Electronics", weight=1.0, supplier_id=2)
        ]
        
        self.promotions = [
            Promotion(promo_id=1, code="SAVE15", discount_percent=15, min_purchase=100, valid_until=datetime.now() + timedelta(days=30), category="Electronics"),
            Promotion(promo_id=2, code="WELCOME10", discount_percent=10, min_purchase=0, valid_until=datetime.now() + timedelta(days=60), category="all"),
            Promotion(promo_id=3, code="EXPIRED", discount_percent=20, min_purchase=50, valid_until=datetime.now() - timedelta(days=1), category="all")
        ]
    
    def test_calculate_order_total_basic(self):
        """Test basic order total calculation"""
        result = self.pricing_service.calculate_order_total(
            order_items=self.order_items,
            customer=self.customer_standard,
            products=self.products,
            promotions=self.promotions,
            shipping_method=ShippingMethod.STANDARD
        )
        
        # Check basic calculations
        self.assertEqual(result["subtotal"].amount, 1459.92)  # 999.99 + 2*29.99 + 5*79.99
        self.assertEqual(result["membership_discount"].amount, 0.0)  # Standard customer
        self.assertEqual(result["promo_discount"].amount, 0.0)  # No promo code
        self.assertAlmostEqual(result["bulk_discount"].amount, 29.1984, places=4)  # 2% for 8 items (5+ tier)
        self.assertEqual(result["loyalty_discount"].amount, 0.0)  # No loyalty points used
        self.assertEqual(result["shipping_cost"].amount, 0.0)  # Free shipping over $50
        self.assertAlmostEqual(result["tax"].amount, 89.4201, places=4)  # 8% of (1459.92 - 29.1984)
        self.assertAlmostEqual(result["total"].amount, 1520.1417, places=4)  # (1459.92 - 29.1984) + 0.0 + 89.4201
    
    def test_calculate_order_total_with_membership_discount(self):
        """Test order total with membership discount"""
        result = self.pricing_service.calculate_order_total(
            order_items=self.order_items,
            customer=self.customer_gold,  # Gold member
            products=self.products,
            promotions=self.promotions,
            shipping_method=ShippingMethod.STANDARD
        )
        
        # Check membership discount
        self.assertEqual(result["membership_discount"].amount, 218.988)  # 15% of 1459.92
        self.assertEqual(result["subtotal_after_membership"].amount, 1240.932)
    
    def test_calculate_order_total_with_promo_discount(self):
        """Test order total with promotional discount"""
        result = self.pricing_service.calculate_order_total(
            order_items=self.order_items,
            customer=self.customer_standard,
            products=self.products,
            promotions=self.promotions,
            promo_code="SAVE15",
            shipping_method=ShippingMethod.STANDARD
        )
        
        # Check promo discount
        self.assertEqual(result["promo_discount"].amount, 218.988)  # 15% of 1459.92 (no membership discount for standard)
        self.assertEqual(result["applied_promotion"].code, "SAVE15")
        self.assertAlmostEqual(result["subtotal_after_promo"].amount, 1240.932, places=4)
    
    def test_calculate_order_total_with_bulk_discount(self):
        """Test order total with bulk discount"""
        # Create order with 10 items
        bulk_order_items = [
            OrderItem(product_id=1, quantity=1, unit_price=999.99),
            OrderItem(product_id=2, quantity=2, unit_price=29.99),
            OrderItem(product_id=3, quantity=5, unit_price=79.99),
            OrderItem(product_id=4, quantity=2, unit_price=49.99)
        ]
        
        result = self.pricing_service.calculate_order_total(
            order_items=bulk_order_items,
            customer=self.customer_standard,
            products=self.products,
            promotions=self.promotions,
            shipping_method=ShippingMethod.STANDARD
        )
        
        # Check bulk discount (5% for 10+ items)
        self.assertAlmostEqual(result["bulk_discount"].amount, 31.198, places=4)  # 2% for 10 items (5+ tier)
        self.assertAlmostEqual(result["subtotal_after_bulk"].amount, 1528.702, places=4)
    
    def test_calculate_order_total_with_loyalty_discount(self):
        """Test order total with loyalty discount"""
        # Add loyalty points to customer
        self.customer_standard.loyalty_points = 200
        
        result = self.pricing_service.calculate_order_total(
            order_items=self.order_items,
            customer=self.customer_standard,
            products=self.products,
            promotions=self.promotions,
            shipping_method=ShippingMethod.STANDARD,
            use_loyalty_points=True,
            loyalty_points_to_use=200
        )
        
        # Check loyalty discount (200 points = $2.00)
        self.assertEqual(result["loyalty_discount"].amount, 2.0)
        self.assertEqual(result["loyalty_points_used"], 200)
        self.assertEqual(result["subtotal_after_loyalty"].amount, 1428.7216)  # After bulk discount
    
    def test_calculate_order_total_with_express_shipping(self):
        """Test order total with express shipping"""
        result = self.pricing_service.calculate_order_total(
            order_items=self.order_items,
            customer=self.customer_standard,
            products=self.products,
            promotions=self.promotions,
            shipping_method=ShippingMethod.EXPRESS
        )
        
        # Check express shipping cost
        expected_shipping = 25.0 + (2.5 + 0.2 + 1.0) * 0.5  # Weight cost with multiplier
        self.assertAlmostEqual(result["shipping_cost"].amount, 28.95, places=4)
    
    def test_calculate_order_total_with_free_shipping(self):
        """Test order total with free shipping"""
        # Create large order over $50
        large_order_items = [
            OrderItem(product_id=1, quantity=1, unit_price=999.99),
            OrderItem(product_id=2, quantity=2, unit_price=29.99),
            OrderItem(product_id=3, quantity=5, unit_price=79.99)
        ]
        
        result = self.pricing_service.calculate_order_total(
            order_items=large_order_items,
            customer=self.customer_standard,
            products=self.products,
            promotions=self.promotions,
            shipping_method=ShippingMethod.STANDARD
        )
        
        # Check free shipping (over $50)
        self.assertEqual(result["shipping_cost"].amount, 0.0)
    
    def test_calculate_order_total_with_expired_promo(self):
        """Test order total with expired promo"""
        result = self.pricing_service.calculate_order_total(
            order_items=self.order_items,
            customer=self.customer_standard,
            products=self.products,
            promotions=self.promotions,
            promo_code="EXPIRED"  # Expired promo
        )
        
        # Check no discount applied
        self.assertEqual(result["promo_discount"].amount, 0.0)
        self.assertIsNone(result["applied_promotion"])
    
    def test_calculate_order_total_with_invalid_promo(self):
        """Test order total with invalid promo"""
        result = self.pricing_service.calculate_order_total(
            order_items=self.order_items,
            customer=self.customer_standard,
            products=self.products,
            promotions=self.promotions,
            promo_code="INVALID"  # Non-existent promo
        )
        
        # Check no discount applied
        self.assertEqual(result["promo_discount"].amount, 0.0)
        self.assertIsNone(result["applied_promotion"])
    
    def test_calculate_tax_by_state(self):
        """Test tax calculation by state"""
        # Test CA tax (7.25%)
        result_ca = self.pricing_service.calculate_order_total(
            order_items=self.order_items,
            customer=self.customer_gold,  # CA address
            products=self.products,
            promotions=self.promotions,
            shipping_method=ShippingMethod.STANDARD
        )
        self.assertAlmostEqual(result_ca["tax"].amount, 88.1682, places=4)  # 7.25% of (1459.92 - 218.988 - 29.1984)
        
        # Test NY tax (4%)
        result_ny = self.pricing_service.calculate_order_total(
            order_items=self.order_items,
            customer=self.customer_silver,  # NY address
            products=self.products,
            promotions=self.promotions,
            shipping_method=ShippingMethod.STANDARD
        )
        self.assertAlmostEqual(result_ny["tax"].amount, 53.2228, places=4)  # 4% of (1459.92 - 29.1984)
        
        # Test TX tax (6.25%)
        result_tx = self.pricing_service.calculate_order_total(
            order_items=self.order_items,
            customer=self.customer_standard,  # TX address
            products=self.products,
            promotions=self.promotions,
            shipping_method=ShippingMethod.STANDARD
        )
        self.assertAlmostEqual(result_tx["tax"].amount, 89.4201, places=4)  # 6.25% of (1459.92 - 29.1984)


if __name__ == '__main__':
    unittest.main()