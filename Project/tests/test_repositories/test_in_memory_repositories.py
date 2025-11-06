import unittest
from datetime import datetime
from domain.models import Customer, Product, Order, OrderItem, Promotion, Supplier
from domain.value_objects import Money
from repositories.in_memory import (
    InMemoryCustomerRepository,
    InMemoryProductRepository,
    InMemoryOrderRepository,
    InMemoryPromotionRepository,
    InMemorySupplierRepository
)


class TestInMemoryRepositories(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.customer_repo = InMemoryCustomerRepository()
        self.product_repo = InMemoryProductRepository()
        self.order_repo = InMemoryOrderRepository()
        self.promotion_repo = InMemoryPromotionRepository()
        self.supplier_repo = InMemorySupplierRepository()
        
        # Add test data
        self.customer_gold = Customer(
            customer_id=101,
            name="Alice Smith",
            email="alice@email.com",
            membership_tier="gold",
            phone="555-0101",
            address="123 Main St, San Francisco CA 94102",
            loyalty_points=100
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
        
        self.order_pending = Order(
            order_id=1,
            customer_id=101,
            items=[OrderItem(product_id=1, quantity=1, unit_price=Money(10.0))],
            status="pending",
            created_at=datetime(2023, 1, 1),
            total_price=Money(100.0),
            shipping_cost=Money(10.0)
        )
        
        self.promotion_save15 = Promotion(
            promo_id=1,
            code="SAVE15",
            discount_percent=15,
            min_purchase=100,
            valid_until=datetime(2025, 12, 31),
            category="Electronics"
        )
        
        self.supplier_tech = Supplier(
            supplier_id=1,
            name="TechDistributor Inc",
            email="orders@techdist.com",
            reliability_score=4.5
        )
        
        # Add test data to repositories
        self.customer_repo.add(self.customer_gold)
        self.product_repo.add(self.product_laptop)
        self.order_repo.add(self.order_pending)
        self.promotion_repo.add(self.promotion_save15)
        self.supplier_repo.add(self.supplier_tech)
    
    def test_customer_repository(self):
        """Test in-memory customer repository"""
        # Test get by ID
        customer = self.customer_repo.get_by_id(101)
        self.assertEqual(customer.customer_id, 101)
        self.assertEqual(customer.name, "Alice Smith")
        
        # Test get all
        all_customers = self.customer_repo.get_all()
        self.assertEqual(len(all_customers), 1)
        self.assertIn(self.customer_gold, all_customers)
        
        # Test update
        updated_customer = Customer(
            customer_id=101,
            name="Alice Smith Updated",
            email="alice.updated@email.com",
            membership_tier="silver",
            phone="555-0101",
            address="123 Main St, San Francisco CA 94102",
            loyalty_points=150
        )
        self.assertTrue(self.customer_repo.update(updated_customer))
        
        # Verify update
        retrieved_customer = self.customer_repo.get_by_id(101)
        self.assertEqual(retrieved_customer.name, "Alice Smith Updated")
        self.assertEqual(retrieved_customer.membership_tier.value, "silver")
        
        # Test delete
        self.assertTrue(self.customer_repo.delete(101))
        self.assertIsNone(self.customer_repo.get_by_id(101))
    
    def test_product_repository(self):
        """Test in-memory product repository"""
        # Test get by ID
        product = self.product_repo.get_by_id(1)
        self.assertEqual(product.product_id, 1)
        self.assertEqual(product.name, "Laptop Pro 15")
        
        # Test get by category
        electronics = self.product_repo.get_by_category("Electronics")
        self.assertEqual(len(electronics), 1)
        self.assertIn(self.product_laptop, electronics)
        
        # Test get in stock
        in_stock = self.product_repo.get_in_stock()
        self.assertEqual(len(in_stock), 1)
        self.assertIn(self.product_laptop, in_stock)
        
        # Test update
        updated_product = Product(
            product_id=1,
            name="Laptop Pro 15 Updated",
            price=1099.99,
            quantity_available=20,
            category="Electronics",
            weight=2.5,
            supplier_id=1
        )
        self.assertTrue(self.product_repo.update(updated_product))
        
        # Verify update
        retrieved_product = self.product_repo.get_by_id(1)
        self.assertEqual(retrieved_product.name, "Laptop Pro 15 Updated")
        self.assertEqual(retrieved_product.price.amount, 1099.99)
    
    def test_order_repository(self):
        """Test in-memory order repository"""
        # Test get by ID
        order = self.order_repo.get_by_id(1)
        self.assertEqual(order.order_id, 1)
        self.assertEqual(order.customer_id, 101)
        
        # Test get by customer
        customer_orders = self.order_repo.get_by_customer(101)
        self.assertEqual(len(customer_orders), 1)
        self.assertIn(self.order_pending, customer_orders)
        
        # Test get by status
        pending_orders = self.order_repo.get_by_status("pending")
        self.assertEqual(len(pending_orders), 1)
        self.assertIn(self.order_pending, pending_orders)
        
        # Test update
        updated_order = Order(
            order_id=1,
            customer_id=101,
            items=[OrderItem(product_id=1, quantity=1, unit_price=Money(10.0))],
            status="confirmed",
            created_at=datetime(2023, 1, 1),
            total_price=Money(100.0),
            shipping_cost=Money(10.0)
        )
        self.assertTrue(self.order_repo.update(updated_order))
        
        # Verify update
        retrieved_order = self.order_repo.get_by_id(1)
        self.assertEqual(retrieved_order.status.value, "confirmed")
    
    def test_promotion_repository(self):
        """Test in-memory promotion repository"""
        # Test get by code
        promotion = self.promotion_repo.get_by_code("SAVE15")
        self.assertEqual(promotion.promo_id, 1)
        self.assertEqual(promotion.discount_percent, 15)
        
        # Test get active
        active_promotions = self.promotion_repo.get_active()
        self.assertEqual(len(active_promotions), 1)
        self.assertIn(self.promotion_save15, active_promotions)
        
        # Test update
        updated_promotion = Promotion(
            promo_id=1,
            code="SAVE20",
            discount_percent=20,
            min_purchase=100,
            valid_until=datetime(2025, 12, 31),
            category="Electronics"
        )
        self.assertTrue(self.promotion_repo.update(updated_promotion))
        
        # Verify update
        retrieved_promotion = self.promotion_repo.get_by_id(1)
        self.assertEqual(retrieved_promotion.code, "SAVE20")
    
    def test_supplier_repository(self):
        """Test in-memory supplier repository"""
        # Test get by ID
        supplier = self.supplier_repo.get_by_id(1)
        self.assertEqual(supplier.supplier_id, 1)
        self.assertEqual(supplier.name, "TechDistributor Inc")
        
        # Test get reliable
        reliable_suppliers = self.supplier_repo.get_reliable(4.0)
        self.assertEqual(len(reliable_suppliers), 1)
        self.assertIn(self.supplier_tech, reliable_suppliers)
        
        # Test update
        updated_supplier = Supplier(
            supplier_id=1,
            name="TechDistributor Inc Updated",
            email="orders.updated@techdist.com",
            reliability_score=4.8
        )
        self.assertTrue(self.supplier_repo.update(updated_supplier))
        
        # Verify update
        retrieved_supplier = self.supplier_repo.get_by_id(1)
        self.assertEqual(retrieved_supplier.reliability_score, 4.8)
    
    def test_order_repository_next_id(self):
        """Test order repository next ID generation"""
        next_id = self.order_repo.get_next_order_id()
        self.assertEqual(next_id, 2)  # First order was ID 1


if __name__ == '__main__':
    unittest.main()