from typing import List, Dict, Any, Optional
from domain.models import Customer, Order


class NotificationSender:
    """Interface for sending notifications"""
    def send_email(self, email_address: str, subject: str, message: str) -> bool:
        """Send an email notification"""
        pass
    
    def send_sms(self, phone_number: str, message: str) -> bool:
        """Send an SMS notification"""
        pass


class OrderNotifier:
    """Interface for order-related notifications"""
    def send_order_confirmation(self, customer: Customer, order: Order) -> bool:
        """Send order confirmation notification"""
        pass
    
    def send_order_status_update(self, customer: Customer, order: Order) -> bool:
        """Send order status update notification"""
        pass
    
    def send_shipping_notification(self, customer: Customer, order: Order) -> bool:
        """Send shipping notification"""
        pass
    
    def send_delivery_notification(self, customer: Customer, order: Order) -> bool:
        """Send delivery notification"""
        pass
    
    def send_cancellation_notification(self, customer: Customer, order: Order, reason: str) -> bool:
        """Send order cancellation notification"""
        pass


class MarketingNotifier:
    """Interface for marketing notifications"""
    def send_marketing_email(self, customers: List[Customer], subject: str, message: str) -> int:
        """Send marketing email to multiple customers"""
        pass


class CustomerNotifier:
    """Interface for customer-related notifications"""
    def send_membership_upgrade_notification(self, customer: Customer, new_tier: str) -> bool:
        """Send membership upgrade notification"""
        pass


class SupplierNotifier:
    """Interface for supplier notifications"""
    def send_low_stock_alert(self, supplier_email: str, product_name: str, current_stock: int) -> bool:
        """Send low stock alert to supplier"""
        pass


class NotificationLogger:
    """Interface for notification logging"""
    def log_notification(self, notification_type: str, recipient: str, subject: str, message: str) -> None:
        """Log a notification for tracking purposes"""
        pass
    
    def get_notification_history(self, notification_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get notification history, optionally filtered by type"""
        pass


class NotificationSettings:
    """Interface for notification settings"""
    def enable_email_notifications(self, enabled: bool) -> None:
        """Enable or disable email notifications"""
        pass
    
    def enable_sms_notifications(self, enabled: bool) -> None:
        """Enable or disable SMS notifications"""
        pass
    
    def is_email_enabled(self) -> bool:
        """Check if email notifications are enabled"""
        pass
    
    def is_sms_enabled(self) -> bool:
        """Check if SMS notifications are enabled"""
        pass