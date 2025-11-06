from typing import Dict, Any, List, Optional, Tuple
from domain.value_objects import Money


class PaymentValidator:
    """Interface for payment validation"""
    def validate_payment_info(self, payment_info: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate payment information"""
        pass
    
    def validate_credit_card(self, payment_info: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate credit card payment information"""
        pass
    
    def validate_paypal(self, payment_info: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate PayPal payment information"""
        pass
    
    def validate_bank_transfer(self, payment_info: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate bank transfer payment information"""
        pass


class PaymentProcessor:
    """Interface for payment processing"""
    def process_payment(
        self, 
        payment_info: Dict[str, Any], 
        amount: Money
    ) -> Tuple[bool, str, Optional[str]]:
        """Process a payment"""
        pass
    
    def refund_payment(self, transaction_id: str, amount: Money) -> Tuple[bool, str]:
        """Refund a payment"""
        pass


class PaymentLogger:
    """Interface for payment logging"""
    def log_payment(self, payment_record: Dict[str, Any]) -> None:
        """Log a payment transaction"""
        pass
    
    def get_payment_history(self) -> List[Dict[str, Any]]:
        """Get all processed payments"""
        pass


class TransactionIdGenerator:
    """Interface for generating transaction IDs"""
    def generate_transaction_id(self) -> str:
        """Generate a unique transaction ID"""
        pass