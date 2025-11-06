import unittest
from domain.models.order_item import (
    OrderItem, 
    DefaultPricingCalculator, 
    NoDiscountCalculator, 
    PercentageDiscountCalculator
)
from domain.value_objects.money import Money


class TestOrderItemRefactored(unittest.TestCase):
    """Test cases for the refactored OrderItem class"""
    
    def test_order_item_creation(self):
        """Test creating an order item with valid data"""
        item = OrderItem(
            product_id=1,
            quantity=2,
            unit_price=10.0,
            weight=1.5
        )
        
        self.assertEqual(item.product_id, 1)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.unit_price, Money(10.0))
        self.assertEqual(item.weight, 1.5)
        self.assertEqual(item.discount_applied, Money(0.0))
    
    def test_order_item_with_money_object(self):
        """Test creating an order item with Money object"""
        price = Money(15.99)
        item = OrderItem(
            product_id=2,
            quantity=3,
            unit_price=price,
            weight=0.5
        )
        
        self.assertEqual(item.unit_price, price)
    
    def test_order_item_validation(self):
        """Test order item validation"""
        # Test invalid product ID
        with self.assertRaises(ValueError) as context:
            OrderItem(product_id=0, quantity=1, unit_price=10.0)
        self.assertIn("Product ID must be positive", str(context.exception))
        
        # Test invalid quantity
        with self.assertRaises(ValueError) as context:
            OrderItem(product_id=1, quantity=0, unit_price=10.0)
        self.assertIn("Quantity must be positive", str(context.exception))
        
        # Test invalid unit price
        with self.assertRaises(ValueError) as context:
            OrderItem(product_id=1, quantity=1, unit_price=-10.0)
        self.assertIn("Unit price must be positive", str(context.exception))
        
        # Test invalid weight
        with self.assertRaises(ValueError) as context:
            OrderItem(product_id=1, quantity=1, unit_price=10.0, weight=-1.0)
        self.assertIn("Weight cannot be negative", str(context.exception))
    
    def test_get_total_price(self):
        """Test calculating total price"""
        item = OrderItem(
            product_id=1,
            quantity=3,
            unit_price=5.0,
            weight=1.0
        )
        
        total = item.get_total_price()
        self.assertEqual(total, Money(15.0))
    
    def test_get_total_price_with_custom_calculator(self):
        """Test calculating total price with custom calculator"""
        class CustomCalculator:
            def calculate_total(self, unit_price, quantity):
                return unit_price.multiply(quantity).add(Money(5.0))  # Add $5 fee
        
        item = OrderItem(
            product_id=1,
            quantity=2,
            unit_price=10.0,
            weight=1.0
        )
        
        total = item.get_total_price(CustomCalculator())
        self.assertEqual(total, Money(25.0))  # 2 * $10 + $5 fee
    
    def test_get_total_price_after_discount(self):
        """Test calculating total price after discount"""
        item = OrderItem(
            product_id=1,
            quantity=2,
            unit_price=10.0,
            weight=1.0
        )
        
        # Apply $3 discount
        item.apply_discount(3.0)
        total_after_discount = item.get_total_price_after_discount()
        self.assertEqual(total_after_discount, Money(17.0))  # $20 - $3
    
    def test_get_total_price_after_discount_with_custom_calculators(self):
        """Test calculating total price after discount with custom calculators"""
        class CustomPricing:
            def calculate_total(self, unit_price, quantity):
                return unit_price.multiply(quantity).multiply(1.1)  # Add 10% tax
        
        class CustomDiscount:
            def calculate_discount(self, total_price):
                return total_price.multiply(0.15)  # 15% discount
        
        item = OrderItem(
            product_id=1,
            quantity=2,
            unit_price=10.0,
            weight=1.0
        )
        
        total_after_discount = item.get_total_price_after_discount(
            CustomPricing(), 
            CustomDiscount()
        )
        # $20 * 1.1 = $22, then 15% off = $18.70
        self.assertEqual(total_after_discount, Money(18.70))
    
    def test_apply_discount(self):
        """Test applying a discount"""
        item = OrderItem(
            product_id=1,
            quantity=2,
            unit_price=10.0,
            weight=1.0
        )
        
        # Apply valid discount
        item.apply_discount(5.0)
        self.assertEqual(item.discount_applied, Money(5.0))
        
        # Apply discount with Money object
        money_discount = Money(3.0)
        item.apply_discount(money_discount)
        self.assertEqual(item.discount_applied, Money(3.0))
    
    def test_apply_discount_validation(self):
        """Test discount validation"""
        item = OrderItem(
            product_id=1,
            quantity=2,
            unit_price=10.0,
            weight=1.0
        )
        
        # Test discount exceeding total price
        with self.assertRaises(ValueError) as context:
            item.apply_discount(25.0)  # Total is $20
        self.assertIn("Discount cannot exceed total price", str(context.exception))
    
    def test_apply_discount_percentage(self):
        """Test applying a discount percentage"""
        item = OrderItem(
            product_id=1,
            quantity=2,
            unit_price=10.0,
            weight=1.0
        )
        
        # Apply 10% discount
        item.apply_discount_percentage(10.0)
        self.assertEqual(item.discount_applied, Money(2.0))  # 10% of $20
    
    def test_apply_discount_percentage_validation(self):
        """Test discount percentage validation"""
        item = OrderItem(
            product_id=1,
            quantity=2,
            unit_price=10.0,
            weight=1.0
        )
        
        # Test invalid percentage
        with self.assertRaises(ValueError) as context:
            item.apply_discount_percentage(-5.0)
        self.assertIn("Discount percent must be between 0 and 100", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            item.apply_discount_percentage(150.0)
        self.assertIn("Discount percent must be between 0 and 100", str(context.exception))
    
    def test_get_total_weight(self):
        """Test calculating total weight"""
        item = OrderItem(
            product_id=1,
            quantity=3,
            unit_price=10.0,
            weight=1.5
        )
        
        total_weight = item.get_total_weight()
        self.assertEqual(total_weight, 4.5)  # 3 * 1.5
    
    def test_update_quantity(self):
        """Test updating quantity"""
        item = OrderItem(
            product_id=1,
            quantity=2,
            unit_price=10.0,
            weight=1.0
        )
        
        # Update to valid quantity
        item.update_quantity(5)
        self.assertEqual(item.quantity, 5)
        
        # Test invalid quantity
        with self.assertRaises(ValueError) as context:
            item.update_quantity(0)
        self.assertIn("Quantity must be positive", str(context.exception))
    
    def test_update_unit_price(self):
        """Test updating unit price"""
        item = OrderItem(
            product_id=1,
            quantity=2,
            unit_price=10.0,
            weight=1.0
        )
        
        # Update to valid price
        item.update_unit_price(15.0)
        self.assertEqual(item.unit_price, Money(15.0))
        
        # Update with Money object
        new_price = Money(20.0)
        item.update_unit_price(new_price)
        self.assertEqual(item.unit_price, new_price)
        
        # Test invalid price
        with self.assertRaises(ValueError) as context:
            item.update_unit_price(-5.0)
        self.assertIn("Unit price must be positive", str(context.exception))
    
    def test_default_pricing_calculator(self):
        """Test default pricing calculator"""
        calculator = DefaultPricingCalculator()
        unit_price = Money(10.0)
        quantity = 3
        
        total = calculator.calculate_total(unit_price, quantity)
        self.assertEqual(total, Money(30.0))
    
    def test_no_discount_calculator(self):
        """Test no discount calculator"""
        calculator = NoDiscountCalculator()
        total_price = Money(50.0)
        
        discount = calculator.calculate_discount(total_price)
        self.assertEqual(discount, Money(0.0))
    
    def test_percentage_discount_calculator(self):
        """Test percentage discount calculator"""
        calculator = PercentageDiscountCalculator(20.0)  # 20% discount
        total_price = Money(100.0)
        
        discount = calculator.calculate_discount(total_price)
        self.assertEqual(discount, Money(20.0))  # 20% of $100
        
        # Test invalid percentage
        with self.assertRaises(ValueError) as context:
            PercentageDiscountCalculator(-10.0)
        self.assertIn("Discount percentage must be between 0 and 100", str(context.exception))


if __name__ == '__main__':
    unittest.main()