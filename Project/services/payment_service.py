import datetime
import uuid
from typing import Dict, Any, Optional, List
from domain.value_objects import Money
from services.interfaces.payment_service_interfaces import (
    PaymentValidator, 
    PaymentProcessor, 
    PaymentLogger, 
    TransactionIdGenerator
)


class DefaultPaymentValidator(PaymentValidator):
    """Default implementation of payment validation"""
    def validate_payment_details(self, payment_method: str, card_number: str, expiry_date: str, cvv: str) -> bool:
        """Validate payment details"""
        if not payment_method or not payment_method.strip():
            return False
        
        payment_method = payment_method.lower()
        
        if payment_method == "credit_card":
            return self._validate_credit_card(card_number, expiry_date, cvv)
        elif payment_method == "debit_card":
            return self._validate_debit_card(card_number, expiry_date, cvv)
        elif payment_method == "paypal":
            return True  # PayPal validation would be handled by PayPal API
        elif payment_method == "bank_transfer":
            return True  # Bank transfer validation would be handled by bank API
        
        return False
    
    def _validate_credit_card(self, card_number: str, expiry_date: str, cvv: str) -> bool:
        """Validate credit card details"""
        if not card_number or not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
            return False
        
        if not expiry_date or not self._validate_expiry_date(expiry_date):
            return False
        
        if not cvv or not cvv.isdigit() or len(cvv) != 3:
            return False
        
        return True
    
    def _validate_debit_card(self, card_number: str, expiry_date: str, cvv: str) -> bool:
        """Validate debit card details"""
        return self._validate_credit_card(card_number, expiry_date, cvv)
    
    def _validate_expiry_date(self, expiry_date: str) -> bool:
        """Validate card expiry date"""
        try:
            if '/' not in expiry_date:
                return False
            
            month, year = expiry_date.split('/')
            if len(month) != 2 or len(year) != 2:
                return False
            
            month = int(month)
            year = int(year) + 2000  # Convert YY to YYYY
            
            current_date = datetime.datetime.now()
            expiry = datetime.datetime(year, month, 1)
            
            # Add one month to expiry to handle end of month
            if month == 12:
                expiry = datetime.datetime(year + 1, 1, 1)
            else:
                expiry = datetime.datetime(year, month + 1, 1)
            
            return expiry > current_date
        except ValueError:
            return False


class DefaultPaymentProcessor(PaymentProcessor):
    """Default implementation of payment processing"""
    def __init__(self, payment_logger: PaymentLogger):
        self.payment_logger = payment_logger
    
    def process_payment(self, amount: Money, payment_method: str, payment_details: Dict[str, str]) -> Dict[str, Any]:
        """Process a payment and return the result"""
        if amount.amount <= 0:
            raise ValueError("Payment amount must be positive")
        
        if not payment_method or not payment_method.strip():
            raise ValueError("Payment method is required")
        
        if not payment_details:
            raise ValueError("Payment details are required")
        
        # In a real implementation, this would integrate with payment gateways
        # For now, we'll simulate the payment process
        
        payment_method = payment_method.lower()
        
        if payment_method in ["credit_card", "debit_card"]:
            return self._process_card_payment(amount, payment_details)
        elif payment_method == "paypal":
            return self._process_paypal_payment(amount, payment_details)
        elif payment_method == "bank_transfer":
            return self._process_bank_transfer(amount, payment_details)
        else:
            raise ValueError(f"Unsupported payment method: {payment_method}")
    
    def _process_card_payment(self, amount: Money, payment_details: Dict[str, str]) -> Dict[str, Any]:
        """Process card payment"""
        card_number = payment_details.get("card_number", "")
        expiry_date = payment_details.get("expiry_date", "")
        cvv = payment_details.get("cvv", "")
        
        # Validate card details
        validator = DefaultPaymentValidator()
        if not validator.validate_payment_details("credit_card", card_number, expiry_date, cvv):
            return {
                "success": False,
                "message": "Invalid card details",
                "transaction_id": None
            }
        
        # Simulate payment processing
        transaction_id = str(uuid.uuid4())
        
        # Log the payment
        self.payment_logger.log_payment(
            transaction_id=transaction_id,
            amount=amount,
            payment_method="credit_card",
            status="success",
            details=payment_details
        )
        
        return {
            "success": True,
            "message": "Payment processed successfully",
            "transaction_id": transaction_id
        }
    
    def _process_paypal_payment(self, amount: Money, payment_details: Dict[str, str]) -> Dict[str, Any]:
        """Process PayPal payment"""
        # In a real implementation, this would integrate with PayPal API
        transaction_id = str(uuid.uuid4())
        
        # Log the payment
        self.payment_logger.log_payment(
            transaction_id=transaction_id,
            amount=amount,
            payment_method="paypal",
            status="success",
            details=payment_details
        )
        
        return {
            "success": True,
            "message": "PayPal payment processed successfully",
            "transaction_id": transaction_id
        }
    
    def _process_bank_transfer(self, amount: Money, payment_details: Dict[str, str]) -> Dict[str, Any]:
        """Process bank transfer"""
        # In a real implementation, this would integrate with bank API
        transaction_id = str(uuid.uuid4())
        
        # Log the payment
        self.payment_logger.log_payment(
            transaction_id=transaction_id,
            amount=amount,
            payment_method="bank_transfer",
            status="pending",
            details=payment_details
        )
        
        return {
            "success": True,
            "message": "Bank transfer initiated successfully",
            "transaction_id": transaction_id
        }
    
    def refund_payment(self, transaction_id: str, amount: Money, reason: str = "") -> Dict[str, Any]:
        """Refund a payment"""
        if not transaction_id or not transaction_id.strip():
            raise ValueError("Transaction ID is required")
        
        if amount.amount <= 0:
            raise ValueError("Refund amount must be positive")
        
        # In a real implementation, this would integrate with payment gateways
        # For now, we'll simulate the refund process
        
        refund_id = str(uuid.uuid4())
        
        # Log the refund
        self.payment_logger.log_refund(
            transaction_id=transaction_id,
            refund_id=refund_id,
            amount=amount,
            reason=reason
        )
        
        return {
            "success": True,
            "message": "Refund processed successfully",
            "refund_id": refund_id
        }


class DefaultPaymentLogger(PaymentLogger):
    """Default implementation of payment logging"""
    def __init__(self):
        self.payment_logs: List[Dict[str, Any]] = []
        self.refund_logs: List[Dict[str, Any]] = []
    
    def log_payment(self, transaction_id: str, amount: Money, payment_method: str, status: str, details: Dict[str, str]) -> None:
        """Log a payment transaction"""
        if not transaction_id or not transaction_id.strip():
            raise ValueError("Transaction ID is required")
        
        if not payment_method or not payment_method.strip():
            raise ValueError("Payment method is required")
        
        if not status or not status.strip():
            raise ValueError("Status is required")
        
        self.payment_logs.append({
            "transaction_id": transaction_id,
            "amount": amount.amount,
            "payment_method": payment_method,
            "status": status,
            "details": details,
            "timestamp": datetime.datetime.now()
        })
    
    def log_refund(self, transaction_id: str, refund_id: str, amount: Money, reason: str) -> None:
        """Log a refund transaction"""
        if not transaction_id or not transaction_id.strip():
            raise ValueError("Transaction ID is required")
        
        if not refund_id or not refund_id.strip():
            raise ValueError("Refund ID is required")
        
        if amount.amount <= 0:
            raise ValueError("Refund amount must be positive")
        
        self.refund_logs.append({
            "transaction_id": transaction_id,
            "refund_id": refund_id,
            "amount": amount.amount,
            "reason": reason,
            "timestamp": datetime.datetime.now()
        })
    
    def get_payment_logs(self, transaction_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get payment logs, optionally filtered by transaction ID"""
        if transaction_id is not None:
            return [log for log in self.payment_logs if log["transaction_id"] == transaction_id]
        return self.payment_logs.copy()
    
    def get_refund_logs(self, transaction_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get refund logs, optionally filtered by transaction ID"""
        if transaction_id is not None:
            return [log for log in self.refund_logs if log["transaction_id"] == transaction_id]
        return self.refund_logs.copy()


class DefaultTransactionIdGenerator(TransactionIdGenerator):
    """Default implementation of transaction ID generation"""
    def generate_transaction_id(self) -> str:
        """Generate a unique transaction ID"""
        return str(uuid.uuid4())


class PaymentService:
    """
    Refactored PaymentService that follows SOLID principles by delegating
    responsibilities to appropriate components.
    """
    
    def __init__(
        self,
        payment_validator: Optional[PaymentValidator] = None,
        payment_processor: Optional[PaymentProcessor] = None,
        payment_logger: Optional[PaymentLogger] = None,
        transaction_id_generator: Optional[TransactionIdGenerator] = None
    ):
        # Use dependency injection for all components
        self.payment_logger = payment_logger or DefaultPaymentLogger()
        self.payment_processor = payment_processor or DefaultPaymentProcessor(self.payment_logger)
        self.payment_validator = payment_validator or DefaultPaymentValidator()
        self.transaction_id_generator = transaction_id_generator or DefaultTransactionIdGenerator()
    
    # Payment validation operations
    def validate_payment_details(self, payment_method: str, card_number: str, expiry_date: str, cvv: str) -> bool:
        """Validate payment details"""
        return self.payment_validator.validate_payment_details(payment_method, card_number, expiry_date, cvv)
    
    # Payment processing operations
    def process_payment(self, amount: Money, payment_method: str, payment_details: Dict[str, str]) -> Dict[str, Any]:
        """Process a payment and return the result"""
        return self.payment_processor.process_payment(amount, payment_method, payment_details)
    
    def refund_payment(self, transaction_id: str, amount: Money, reason: str = "") -> Dict[str, Any]:
        """Refund a payment"""
        return self.payment_processor.refund_payment(transaction_id, amount, reason)
    
    # Payment logging operations
    def log_payment(self, transaction_id: str, amount: Money, payment_method: str, status: str, details: Dict[str, str]) -> None:
        """Log a payment transaction"""
        self.payment_logger.log_payment(transaction_id, amount, payment_method, status, details)
    
    def log_refund(self, transaction_id: str, refund_id: str, amount: Money, reason: str) -> None:
        """Log a refund transaction"""
        self.payment_logger.log_refund(transaction_id, refund_id, amount, reason)
    
    def get_payment_logs(self, transaction_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get payment logs, optionally filtered by transaction ID"""
        return self.payment_logger.get_payment_logs(transaction_id)
    
    def get_refund_logs(self, transaction_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get refund logs, optionally filtered by transaction ID"""
        return self.payment_logger.get_refund_logs(transaction_id)
    
    # Transaction ID generation operations
    def generate_transaction_id(self) -> str:
        """Generate a unique transaction ID"""
        return self.transaction_id_generator.generate_transaction_id()