from domain.models import Customer
from domain.value_objects import Money


class LoyaltyDiscountStrategy:
    def __init__(self, max_discount_percent: float = 10.0, points_per_dollar: int = 100):
        """
        Initialize loyalty discount strategy
        :param max_discount_percent: Maximum discount percentage (default 10%)
        :param points_per_dollar: Points needed for $1 discount (default 100)
        """
        self.max_discount_percent = max_discount_percent
        self.points_per_dollar = points_per_dollar
    
    def apply_discount(self, subtotal: Money, customer: Customer, use_all_points: bool = False, points_to_use: int = 0) -> tuple[Money, int]:
        """
        Apply loyalty points discount
        :param subtotal: Order subtotal
        :param customer: Customer object
        :param use_all_points: If True, use maximum possible points
        :param points_to_use: Specific number of points to use (when use_all_points is False)
        :return: Tuple of (discount_amount, points_used)
        """
        if customer.loyalty_points <= 0:
            return Money(0.0), 0
        
        # Calculate maximum discount based on percentage
        max_discount_amount = subtotal.multiply(self.max_discount_percent / 100)
        
        # Calculate maximum discount based on available points
        max_points_discount = Money(customer.loyalty_points / self.points_per_dollar)
        
        # Use the smaller of the two limits
        if use_all_points:
            # Use as many points as possible (up to max discount)
            if max_points_discount.is_greater_than(max_discount_amount):
                discount_amount = max_discount_amount
                points_used = int(discount_amount.amount * self.points_per_dollar)
            else:
                discount_amount = max_points_discount
                points_used = customer.loyalty_points
        else:
            # Use specified points (up to max discount)
            points_to_use = min(points_to_use, customer.loyalty_points)
            points_discount = Money(points_to_use / self.points_per_dollar)
            
            if points_discount.is_greater_than(max_discount_amount):
                discount_amount = max_discount_amount
                points_used = int(discount_amount.amount * self.points_per_dollar)
            else:
                discount_amount = points_discount
                points_used = points_to_use
        
        return discount_amount, points_used
    
    def get_points_needed_for_discount(self, discount_amount: Money) -> int:
        """Calculate points needed for a specific discount amount"""
        return int(discount_amount.amount * self.points_per_dollar)
    
    def get_max_discount_for_points(self, points: int) -> Money:
        """Calculate maximum discount for a given number of points"""
        return Money(points / self.points_per_dollar)