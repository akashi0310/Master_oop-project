import unittest
from domain.value_objects.email import Email

class TestEmail(unittest.TestCase):
    def test_email_creation_valid(self):
        email = Email("test@example.com")
        self.assertEqual(email.value, "test@example.com")

    def test_email_creation_invalid_empty_string(self):
        with self.assertRaisesRegex(ValueError, "Email value must be a non-empty string."):
            Email("")

    def test_email_creation_invalid_format_no_at_symbol(self):
        with self.assertRaisesRegex(ValueError, "Invalid email format."):
            Email("testexample.com")

    def test_email_creation_invalid_format_no_domain(self):
        with self.assertRaisesRegex(ValueError, "Invalid email format."):
            Email("test@.com")

    def test_email_creation_invalid_format_no_tld(self):
        with self.assertRaisesRegex(ValueError, "Invalid email format."):
            Email("test@example")

    def test_email_equality(self):
        email1 = Email("test@example.com")
        email2 = Email("test@example.com")
        email3 = Email("another@example.com")
        self.assertEqual(email1, email2)
        self.assertNotEqual(email1, email3)

if __name__ == '__main__':
    unittest.main()