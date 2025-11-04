class PaymentService:
    def validate_payment(self, payment_info, total):
        if not payment_info.get("valid"):
            raise ValueError("Invalid payment info")

        if payment_info.get("amount", 0) < total:
            raise ValueError("Insufficient payment amount")

        if payment_info.get("type") == "credit_card":
            if len(payment_info.get("card_number", "")) < 16:
                raise ValueError("Invalid card number")
        elif payment_info.get("type") == "paypal":
            if not payment_info.get("email"):
                raise ValueError("PayPal email required")
        else:
            raise ValueError("Unsupported payment type")
