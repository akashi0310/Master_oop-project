class ShippingService:
    def calculate_shipping(self, subtotal, total_weight, method, customer):
        if method == 'express':
            cost = 25 + total_weight * 0.5
            if customer.membership_tier == 'gold':
                cost *= 0.5
        elif method == 'standard':
            cost = 0 if subtotal >= 50 else 5 + total_weight * 0.2
        elif method == 'overnight':
            cost = 50 + total_weight * 1.0
        else:
            raise ValueError("Invalid shipping method")
        return cost
