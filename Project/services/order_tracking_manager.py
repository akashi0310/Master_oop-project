from typing import Optional


class OrderTrackingManager:
    """Manages order tracking information"""
    
    def __init__(self):
        self._tracking_number: Optional[str] = None
        self._payment_method: Optional[str] = None
    
    @property
    def tracking_number(self) -> Optional[str]:
        """Get the tracking number"""
        return self._tracking_number
    
    @property
    def payment_method(self) -> Optional[str]:
        """Get the payment method"""
        return self._payment_method
    
    def add_tracking_number(self, tracking_number: str) -> None:
        """Add a tracking number to the order"""
        if not tracking_number or not tracking_number.strip():
            raise ValueError("Tracking number cannot be empty")
        self._tracking_number = tracking_number.strip()
    
    def set_payment_method(self, payment_method: str) -> None:
        """Set the payment method for the order"""
        if not payment_method or not payment_method.strip():
            raise ValueError("Payment method cannot be empty")
        self._payment_method = payment_method.strip()