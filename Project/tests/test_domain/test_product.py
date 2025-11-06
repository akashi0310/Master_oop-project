import unittest
from domain.models.product import Product
from domain.value_objects.money import Money
from domain.enums.membership_tier import MembershipTier
from services.product_validator import DefaultProductValidator


class TestProductRefactored(unittest.TestCase):
    """Test cases for the refactored Product class"""
    
    def test_product_creation(self):
        """Test creating a product with valid data"""
        product = Product(
            product_id=1,
            name="Test Product",
            price=99.99,
            quantity_available=10,
            category="Electronics",
            weight=1.5,
            supplier_id=1
        )
        
        self.assertEqual(product.product_id, 1)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, Money(99.99))
        self.assertEqual(product.quantity_available, 10)
        self.assertEqual(product.category, "Electronics")
        self.assertEqual(product.weight, 1.5)
        self.assertEqual(product.supplier_id, 1)
        self.assertTrue(product.discount_eligible)
    
    def test_product_with_money_object(self):
        """Test creating a product with Money object"""
        price = Money(149.99)
        product = Product(
            product_id=2,
            name="Premium Product",
            price=price,
            quantity_available=5,
            category="Luxury",
            weight=2.0,
            supplier_id=2
        )
        
        self.assertEqual(product.price, price)
        self.assertEqual(product.price.amount, 149.99)
    
    def test_product_validation(self):
        """Test product validation"""
        # Test invalid product ID
        with self.assertRaises(ValueError) as context:
            Product(
                product_id=0,
                name="Test",
                price=10.0,
                quantity_available=5,
                category="Test",
                weight=1.0,
                supplier_id=1
            )
        
        # Test empty name
        with self.assertRaises(ValueError) as context:
            Product(
                product_id=1,
                name="",
                price=10.0,
                quantity_available=5,
                category="Test",
                weight=1.0,
                supplier_id=1
            )
        
        # Test negative quantity
        with self.assertRaises(ValueError) as context:
            Product(
                product_id=1,
                name="Test",
                price=10.0,
                quantity_available=-1,
                category="Test",
                weight=1.0,
                supplier_id=1
            )
        
        # Test negative weight
        with self.assertRaises(ValueError) as context:
            Product(
                product_id=1,
                name="Test",
                price=10.0,
                quantity_available=5,
                category="Test",
                weight=-1.0,
                supplier_id=1
            )
        
        # Test invalid supplier ID
        with self.assertRaises(ValueError) as context:
            Product(
                product_id=1,
                name="Test",
                price=10.0,
                quantity_available=5,
                category="Test",
                weight=1.0,
                supplier_id=0
            )
        
        # Test empty category
        with self.assertRaises(ValueError) as context:
            Product(
                product_id=1,
                name="Test",
                price=10.0,
                quantity_available=5,
                category="",
                weight=1.0,
                supplier_id=1
            )
    
    def test_stock_operations(self):
        """Test stock management operations"""
        product = Product(
            product_id=1,
            name="Test Product",
            price=10.0,
            quantity_available=10,
            category="Test",
            weight=1.0,
            supplier_id=1
        )
        
        # Test in stock check
        self.assertTrue(product.is_in_stock())
        
        # Test sufficient stock
        self.assertTrue(product.has_sufficient_stock(5))
        self.assertFalse(product.has_sufficient_stock(15))
        
        # Test reduce stock
        product.reduce_stock(3)
        self.assertEqual(product.quantity_available, 7)
        
        # Test low stock after reduction
        self.assertTrue(product.is_low_stock(threshold=10))
        self.assertFalse(product.is_low_stock(threshold=5))
        
        # Test increase stock
        product.increase_stock(5)
        self.assertEqual(product.quantity_available, 12)
        
        # Test low stock after increase (should not be low stock anymore)
        self.assertFalse(product.is_low_stock(threshold=10))
        self.assertFalse(product.is_low_stock(threshold=5))
    
    def test_pricing_operations(self):
        """Test pricing operations"""
        product = Product(
            product_id=1,
            name="Test Product",
            price=10.0,
            quantity_available=10,
            category="Test",
            weight=1.0,
            supplier_id=1
        )
        
        # Test update price with float
        product.update_price(15.0)
        self.assertEqual(product.price, Money(15.0))
        
        # Test update price with Money object
        new_price = Money(20.0)
        product.update_price(new_price)
        self.assertEqual(product.price, new_price)
        
        # Test discount eligibility
        self.assertTrue(product.discount_eligible)
        product.set_discount_eligibility(False)
        self.assertFalse(product.discount_eligible)
    
    def test_total_value_calculation(self):
        """Test total value calculation"""
        product = Product(
            product_id=1,
            name="Test Product",
            price=10.0,
            quantity_available=5,
            category="Test",
            weight=1.0,
            supplier_id=1
        )
        
        total_value = product.get_total_value()
        self.assertEqual(total_value, Money(50.0))
    
    def test_custom_validator(self):
        """Test using a custom validator"""
        class StrictValidator(DefaultProductValidator):
            def validate_product_data(
                self,
                product_id: int,
                name: str,
                quantity_available: int,
                weight: float,
                supplier_id: int,
                category: str
            ) -> None:
                super().validate_product_data(
                    product_id, name, quantity_available, weight, supplier_id, category
                )
                if len(name) < 5:
                    raise ValueError("Name must be at least 5 characters long")
        
        # Test with valid data
        product = Product(
            product_id=1,
            name="Valid Name",
            price=10.0,
            quantity_available=5,
            category="Test",
            weight=1.0,
            supplier_id=1,
            validator=StrictValidator()
        )
        self.assertEqual(product.name, "Valid Name")
        
        # Test with invalid data for custom validator
        with self.assertRaises(ValueError) as context:
            Product(
                product_id=1,
                name="Bad",
                price=10.0,
                quantity_available=5,
                category="Test",
                weight=1.0,
                supplier_id=1,
                validator=StrictValidator()
            )
    
    def test_error_handling(self):
        """Test error handling in stock operations"""
        product = Product(
            product_id=1,
            name="Test Product",
            price=10.0,
            quantity_available=10,
            category="Test",
            weight=1.0,
            supplier_id=1
        )
        
        # Test reducing more than available
        with self.assertRaises(ValueError) as context:
            product.reduce_stock(15)
        
        # Test reducing negative quantity
        with self.assertRaises(ValueError) as context:
            product.reduce_stock(-1)
        
        # Test increasing negative quantity
        with self.assertRaises(ValueError) as context:
            product.increase_stock(-1)
        
        # Test checking insufficient stock with negative quantity
        with self.assertRaises(ValueError) as context:
            product.has_sufficient_stock(-1)
    
    def test_repr(self):
        """Test string representation"""
        product = Product(
            product_id=1,
            name="Test Product",
            price=10.0,
            quantity_available=5,
            category="Test",
            weight=1.0,
            supplier_id=1
        )
        
        expected = "<Product Test Product (USD 10.00)>"
        self.assertEqual(repr(product), expected)


if __name__ == '__main__':
    unittest.main()