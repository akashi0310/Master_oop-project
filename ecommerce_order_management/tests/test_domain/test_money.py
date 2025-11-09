import unittest
from domain.value_objects.money import Money

class TestMoney(unittest.TestCase):
    def test_money_creation_valid(self):
        money = Money(amount=100.50, currency="USD")
        self.assertEqual(money.amount, 100.50)
        self.assertEqual(money.currency, "USD")

    def test_money_creation_default_currency(self):
        money = Money(amount=50)
        self.assertEqual(money.amount, 50.0)
        self.assertEqual(money.currency, "USD")

    def test_money_creation_invalid_negative_amount(self):
        with self.assertRaisesRegex(ValueError, "Amount must be a non-negative number."):
            Money(amount=-10.0)

    def test_money_creation_invalid_non_numeric_amount(self):
        with self.assertRaisesRegex(ValueError, "Amount must be a non-negative number."):
            Money(amount="abc")

    def test_money_creation_invalid_empty_currency(self):
        with self.assertRaisesRegex(ValueError, "Currency must be a non-empty string."):
            Money(amount=100, currency="")

    def test_money_addition(self):
        m1 = Money(100, "USD")
        m2 = Money(50, "USD")
        result = m1 + m2
        self.assertEqual(result, Money(150, "USD"))

    def test_money_addition_different_currency_raises_error(self):
        m1 = Money(100, "USD")
        m2 = Money(50, "EUR")
        with self.assertRaisesRegex(ValueError, "Cannot add money of different currencies."):
            _ = m1 + m2

    def test_money_subtract(self):
        m1 = Money(100, "USD")
        m2 = Money(50, "USD")
        result = m1 - m2
        self.assertEqual(result, Money(50, "USD"))

    def test_money_subtract_different_currency_raises_error(self):
        m1 = Money(100, "USD")
        m2 = Money(50, "EUR")
        with self.assertRaisesRegex(ValueError, "Cannot subtract money of different currencies."):
            _ = m1 - m2

    def test_money_multiplication(self):
        m1 = Money(100, "USD")
        result = m1 * 2
        self.assertEqual(result, Money(200, "USD"))

    def test_money_multiplication_float(self):
        m1 = Money(100, "USD")
        result = m1 * 1.5
        self.assertEqual(result, Money(150, "USD"))

    def test_money_multiplication_invalid_scalar(self):
        m1 = Money(100, "USD")
        with self.assertRaisesRegex(ValueError, "Can only multiply Money by a numeric scalar."):
            _ = m1 * "abc"

    def test_money_division(self):
        m1 = Money(100, "USD")
        result = m1 / 2
        self.assertEqual(result, Money(50, "USD"))

    def test_money_division_float(self):
        m1 = Money(100, "USD")
        result = m1 / 2.5
        self.assertEqual(result, Money(40, "USD"))

    def test_money_division_by_zero_raises_error(self):
        m1 = Money(100, "USD")
        with self.assertRaisesRegex(ValueError, "Can only divide Money by a non-zero numeric scalar."):
            _ = m1 / 0

    def test_money_equality(self):
        m1 = Money(100, "USD")
        m2 = Money(100, "USD")
        m3 = Money(100, "EUR")
        m4 = Money(50, "USD")
        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)
        self.assertNotEqual(m1, m4)

    def test_money_less_than(self):
        m1 = Money(50, "USD")
        m2 = Money(100, "USD")
        self.assertLess(m1, m2)
        self.assertFalse(m2 < m1)

    def test_money_less_than_different_currency_raises_error(self):
        m1 = Money(50, "USD")
        m2 = Money(100, "EUR")
        with self.assertRaisesRegex(ValueError, "Cannot compare money of different currencies."):
            _ = m1 < m2

    def test_money_less_than_or_equal(self):
        m1 = Money(50, "USD")
        m2 = Money(100, "USD")
        m3 = Money(50, "USD")
        self.assertLessEqual(m1, m2)
        self.assertLessEqual(m1, m3)
        self.assertFalse(m2 <= m1)

    def test_money_greater_than(self):
        m1 = Money(100, "USD")
        m2 = Money(50, "USD")
        self.assertGreater(m1, m2)
        self.assertFalse(m2 > m1)

    def test_money_greater_than_or_equal(self):
        m1 = Money(100, "USD")
        m2 = Money(50, "USD")
        m3 = Money(100, "USD")
        self.assertGreaterEqual(m1, m2)
        self.assertGreaterEqual(m1, m3)
        self.assertFalse(m2 >= m1)

if __name__ == '__main__':
    unittest.main()