import unittest
from domain.models import Product
from domain.value_objects import Money


class TestProduct(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
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
            supplier_id=2
        )
        
        self.product_out_of_stock = Product(
            product_id=3,
            name="Out of Stock Item",
            price=19.99,
            quantity_available=0,
            category="Electronics",
            weight=1.0,
            supplier_id=2
        )
    
    def test_product_creation(self):
        """Test product creation with valid data"""
        product = Product(
            product_id=4,
            name="Mechanical Keyboard",
            price=79.99,
            quantity_available=30,
            category="Electronics",
            weight=1.0,
            supplier_id=2
        )
        
        self.assertEqual(product.product_id, 4)
        self.assertEqual(product.name, "Mechanical Keyboard")
        self.assertEqual(product.price.amount, 79.99)
        self.assertEqual(product.quantity_available, 30)
        self.assertEqual(product.category, "Electronics")
        self.assertEqual(product.weight, 1.0)
        self.assertEqual(product.supplier_id, 2)
        self.assertTrue(product.discount_eligible)
    
    def test_product_creation_invalid_data(self):
        """Test product creation with invalid data"""
        with self.assertRaises(ValueError):
            Product(
                product_id=-1,  # Invalid ID
                name="Test",
                price=29.99,
                quantity_available=30,
                category="Electronics",
                weight=1.0,
                supplier_id=2
            )
        
        with self.assertRaises(ValueError):
            Product(
                product_id=5,
                name="",  # Empty name
                price=29.99,
                quantity_available=30,
                category="Electronics",
                weight=1.0,
                supplier_id=2
            )
        
        with self.assertRaises(ValueError):
            Product(
                product_id=6,
                name="Test",
                price=-10.99,  # Negative price
                quantity_available=30,
                category="Electronics",
                weight=1.0,
                supplier_id=2
            )
        
        with self.assertRaises(ValueError):
            Product(
                product_id=7,
                name="Test",
                price=29.99,
                quantity_available=-5,  # Negative quantity
                category="Electronics",
                weight=1.0,
                supplier_id=2
            )
        
        with self.assertRaises(ValueError):
            Product(
                product_id=8,
                name="Test",
                price=29.99,
                quantity_available=30,
                category="",  # Empty category
                weight=1.0,
                supplier_id=2
            )
        
        with self.assertRaises(ValueError):
            Product(
                product_id=9,
                name="Test",
                price=29.99,
                quantity_available=30,
                category="Electronics",
                weight=-1.0,  # Negative weight
                supplier_id=2
            )
        
        with self.assertRaises(ValueError):
            Product(
                product_id=10,
                name="Test",
                price=29.99,
                quantity_available=30,
                category="Electronics",
                weight=1.0,
                supplier_id=-1  # Negative supplier ID
            )
    
    def test_is_in_stock(self):
        """Test if product is in stock"""
        self.assertTrue(self.product_laptop.is_in_stock())
        self.assertTrue(self.product_mouse.is_in_stock())
        self.assertFalse(self.product_out_of_stock.is_in_stock())
    
    def test_has_sufficient_stock(self):
        """Test if product has sufficient stock"""
        self.assertTrue(self.product_laptop.has_sufficient_stock(5))
        self.assertTrue(self.product_laptop.has_sufficient_stock(15))
        self.assertFalse(self.product_laptop.has_sufficient_stock(20))
        self.assertFalse(self.product_out_of_stock.has_sufficient_stock(1))
    
    def test_reduce_stock(self):
        """Test reducing product stock"""
        initial_quantity = self.product_laptop.quantity_available
        self.product_laptop.reduce_stock(5)
        self.assertEqual(self.product_laptop.quantity_available, initial_quantity - 5)
        
        # Test reducing too much stock
        with self.assertRaises(ValueError):
            self.product_laptop.reduce_stock(20)
    
    def test_increase_stock(self):
        """Test increasing product stock"""
        initial_quantity = self.product_laptop.quantity_available
        self.product_laptop.increase_stock(10)
        self.assertEqual(self.product_laptop.quantity_available, initial_quantity + 10)
        
        # Test invalid increase amount
        with self.assertRaises(ValueError):
            self.product_laptop.increase_stock(-5)
    
    def test_update_price(self):
        """Test updating product price"""
        new_price = Money(899.99)
        self.product_laptop.update_price(new_price)
        self.assertEqual(self.product_laptop.price.amount, 899.99)
        
        # Test invalid price
        with self.assertRaises(ValueError):
            self.product_laptop.update_price(Money(-100))
    
    def test_is_low_stock(self):
        """Test low stock detection"""
        self.assertTrue(self.product_out_of_stock.is_low_stock(10))
        self.assertFalse(self.product_laptop.is_low_stock(10))
        self.assertFalse(self.product_mouse.is_low_stock(5))
    
    def test_get_total_value(self):
        """Test calculating total inventory value"""
        expected_value = self.product_laptop.price.multiply(self.product_laptop.quantity_available)
        actual_value = self.product_laptop.get_total_value()
        self.assertEqual(actual_value.amount, expected_value.amount)
    
    def test_repr(self):
        """Test product string representation"""
        expected = f"<Product {self.product_laptop.name} ({self.product_laptop.price})>"
        self.assertEqual(repr(self.product_laptop), expected)


if __name__ == '__main__':
    unittest.main()