from domain.models import Customer
from domain.value_objects import Money


class MembershipDiscountStrategy:
    def apply_discount(self, subtotal: Money, customer: Customer) -> Money:
        """Apply membership discount based on customer's tier"""
        discount_rate = customer.get_membership_discount_rate()
        if discount_rate > 0:
            return subtotal.multiply(discount_rate)
        return Money(0.0)