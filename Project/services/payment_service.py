from typing import Dict, Any, List, Optional
from datetime import datetime
from domain.value_objects import Money


class PaymentService:
    def __init__(self):
        self.payment_methods = ["credit_card", "paypal", "bank_transfer"]
        self.processed_payments: List[Dict[str, Any]] = []
    
    def validate_payment_info(self, payment_info: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate payment information
        Returns a tuple of (is_valid, error_message)
        """
        if not payment_info.get("valid", False):
            return False, "Payment information is marked as invalid"
        
        payment_type = payment_info.get("type", "").lower()
        if payment_type not in self.payment_methods:
            return False, f"Unsupported payment method: {payment_type}"
        
        # Validate based on payment type
        if payment_type == "credit_card":
            return self._validate_credit_card(payment_info)
        elif payment_type == "paypal":
            return self._validate_paypal(payment_info)
        elif payment_type == "bank_transfer":
            return self._validate_bank_transfer(payment_info)
        
        return False, "Unknown payment method"
    
    def _validate_credit_card(self, payment_info: Dict[str, Any]) -> tuple[bool, str]:
        """Validate credit card payment information"""
        card_number = payment_info.get("card_number", "")
        if not card_number:
            return False, "Credit card number is required"
        
        # Basic validation (in real system, would use Luhn algorithm)
        if len(card_number) < 16 or len(card_number) > 19:
            return False, "Invalid credit card number length"
        
        if not card_number.isdigit():
            return False, "Credit card number must contain only digits"
        
        expiry_date = payment_info.get("expiry_date", "")
        if not expiry_date:
            return False, "Expiry date is required"
        
        cvv = payment_info.get("cvv", "")
        if not cvv or len(cvv) != 3 or not cvv.isdigit():
            return False, "Valid CVV is required"
        
        return True, ""
    
    def _validate_paypal(self, payment_info: Dict[str, Any]) -> tuple[bool, str]:
        """Validate PayPal payment information"""
        email = payment_info.get("email", "")
        if not email:
            return False, "PayPal email is required"
        
        # Basic email validation
        if "@" not in email or "." not in email:
            return False, "Invalid PayPal email format"
        
        return True, ""
    
    def _validate_bank_transfer(self, payment_info: Dict[str, Any]) -> tuple[bool, str]:
        """Validate bank transfer payment information"""
        account_number = payment_info.get("account_number", "")
        if not account_number:
            return False, "Bank account number is required"
        
        routing_number = payment_info.get("routing_number", "")
        if not routing_number:
            return False, "Bank routing number is required"
        
        return True, ""
    
    def process_payment(
        self, 
        payment_info: Dict[str, Any], 
        amount: Money
    ) -> tuple[bool, str, Optional[str]]:
        """
        Process a payment
        Returns a tuple of (success, message, transaction_id)
        """
        # Validate payment info
        is_valid, error_message = self.validate_payment_info(payment_info)
        if not is_valid:
            return False, error_message, None
        
        # Check payment amount
        payment_amount = payment_info.get("amount", 0)
        if payment_amount < amount.amount:
            return False, f"Insufficient payment amount. Required: ${amount.amount:.2f}", None
        
        # Process payment (in real system, would integrate with payment gateway)
        transaction_id = self._generate_transaction_id()
        
        # Record payment
        payment_record = {
            "transaction_id": transaction_id,
            "payment_type": payment_info.get("type"),
            "amount": amount.amount,
            "timestamp": datetime.datetime.now(),
            "status": "completed"
        }
        self.processed_payments.append(payment_record)
        
        return True, "Payment processed successfully", transaction_id
    
    def refund_payment(self, transaction_id: str, amount: Money) -> tuple[bool, str]:
        """
        Refund a payment
        Returns a tuple of (success, message)
        """
        # Find the payment record
        payment_record = None
        for record in self.processed_payments:
            if record["transaction_id"] == transaction_id:
                payment_record = record
                break
        
        if not payment_record:
            return False, "Transaction not found"
        
        if payment_record["status"] != "completed":
            return False, "Cannot refund a payment that is not completed"
        
        # Process refund (in real system, would integrate with payment gateway)
        refund_id = self._generate_transaction_id()
        
        # Update payment record
        payment_record["status"] = "refunded"
        payment_record["refund_id"] = refund_id
        payment_record["refund_amount"] = amount.amount
        payment_record["refund_timestamp"] = datetime.datetime.now()
        
        return True, f"Refund processed successfully. Refund ID: {refund_id}"
    
    def get_payment_history(self) -> List[Dict[str, Any]]:
        """Get all processed payments"""
        return self.processed_payments.copy()
    
    def _generate_transaction_id(self) -> str:
        """Generate a unique transaction ID"""
        import uuid
        return str(uuid.uuid4())
