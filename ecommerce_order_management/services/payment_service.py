from typing import Dict, Any
from ecommerce_order_management.domain.models.order import Order
from ecommerce_order_management.domain.value_objects.money import Money

class PaymentService:
    def process_payment(self, order: Order, payment_info: Dict[str, Any]) -> bool:
        if not payment_info.get("valid"):
            return False

        if payment_info.get("type") == "credit_card":
            if len(payment_info.get("card_number", "")) < 16:
                return False
        elif payment_info.get("type") == "paypal":
            if not payment_info.get("email"):
                return False

        if payment_info.get("amount", 0.0) < order.total_price.amount:
            return False
        
        # Simulate payment processing
        print(f"Processing payment for order {order.order_id} with amount {order.total_price.amount} via {payment_info.get('type')}")
        return True