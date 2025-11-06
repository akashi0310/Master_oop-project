from typing import List, Dict, Any, Optional
from datetime import datetime
from domain.models import Customer, Order
from services.interfaces.notification_service_interfaces import (
    NotificationSender, 
    OrderNotifier, 
    MarketingNotifier, 
    CustomerNotifier, 
    SupplierNotifier, 
    NotificationLogger, 
    NotificationSettings
)


class DefaultNotificationSender(NotificationSender):
    """Default implementation of notification sending"""
    def send_email(self, email_address: str, subject: str, message: str) -> bool:
        """Send an email notification"""
        # In a real system, this would integrate with an email service
        print(f"Email to {email_address}: {subject} - {message}")
        return True
    
    def send_sms(self, phone_number: str, message: str) -> bool:
        """Send an SMS notification"""
        # In a real system, this would integrate with an SMS service
        print(f"SMS to {phone_number}: {message}")
        return True


class DefaultOrderNotifier(OrderNotifier):
    """Default implementation of order notifications"""
    def __init__(self, notification_sender: NotificationSender):
        self.notification_sender = notification_sender
    
    def send_order_confirmation(self, customer: Customer, order: Order) -> bool:
        """Send order confirmation notification"""
        message = f"Order {order.order_id} confirmed! Total: ${order.total_price.amount:.2f}"
        return self.notification_sender.send_email(customer.email.value, f"Order Confirmation", message)
    
    def send_order_status_update(self, customer: Customer, order: Order) -> bool:
        """Send order status update notification"""
        message = f"Order {order.order_id} status changed to {order.status.value}"
        return self.notification_sender.send_email(customer.email.value, f"Order Status Update", message)
    
    def send_shipping_notification(self, customer: Customer, order: Order) -> bool:
        """Send shipping notification"""
        success = False
        
        # Send email notification
        message = f"Order {order.order_id} has been shipped! Tracking: {order.tracking_number}"
        success = self.notification_sender.send_email(customer.email.value, f"Order Shipped", message)
        
        # Send SMS notification if phone number is available
        if customer.phone:
            sms_message = f"Order {order.order_id} shipped. Track: {order.tracking_number}"
            success = self.notification_sender.send_sms(customer.phone, sms_message) or success
        
        return success
    
    def send_delivery_notification(self, customer: Customer, order: Order) -> bool:
        """Send delivery notification"""
        message = f"Order {order.order_id} has been delivered! Thank you for your purchase."
        return self.notification_sender.send_email(customer.email.value, f"Order Delivered", message)
    
    def send_cancellation_notification(self, customer: Customer, order: Order, reason: str) -> bool:
        """Send order cancellation notification"""
        message = f"Order {order.order_id} has been cancelled. Reason: {reason}"
        return self.notification_sender.send_email(customer.email.value, f"Order Cancelled", message)


class DefaultMarketingNotifier(MarketingNotifier):
    """Default implementation of marketing notifications"""
    def __init__(self, notification_sender: NotificationSender):
        self.notification_sender = notification_sender
    
    def send_marketing_email(self, customers: List[Customer], subject: str, message: str) -> int:
        """Send marketing email to multiple customers"""
        success_count = 0
        for customer in customers:
            if self.notification_sender.send_email(customer.email.value, subject, message):
                success_count += 1
        return success_count


class DefaultCustomerNotifier(CustomerNotifier):
    """Default implementation of customer notifications"""
    def __init__(self, notification_sender: NotificationSender):
        self.notification_sender = notification_sender
    
    def send_membership_upgrade_notification(self, customer: Customer, new_tier: str) -> bool:
        """Send membership upgrade notification"""
        message = f"Congratulations! You've been upgraded to {new_tier} membership!"
        return self.notification_sender.send_email(customer.email.value, f"Membership Upgrade", message)


class DefaultSupplierNotifier(SupplierNotifier):
    """Default implementation of supplier notifications"""
    def __init__(self, notification_sender: NotificationSender):
        self.notification_sender = notification_sender
    
    def send_low_stock_alert(self, supplier_email: str, product_name: str, current_stock: int) -> bool:
        """Send low stock alert to supplier"""
        message = f"Low stock alert for {product_name}. Current stock: {current_stock}"
        return self.notification_sender.send_email(supplier_email, f"Low Stock Alert", message)


class DefaultNotificationLogger(NotificationLogger):
    """Default implementation of notification logging"""
    def __init__(self):
        self.notification_history: List[Dict[str, Any]] = []
    
    def log_notification(self, notification_type: str, recipient: str, subject: str, message: str) -> None:
        """Log a notification for tracking purposes"""
        notification = {
            'type': notification_type,
            'recipient': recipient,
            'subject': subject,
            'message': message,
            'timestamp': datetime.now(),
            'status': 'sent'
        }
        self.notification_history.append(notification)
    
    def get_notification_history(self, notification_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get notification history, optionally filtered by type"""
        if notification_type:
            return [n for n in self.notification_history if n['type'] == notification_type]
        return self.notification_history.copy()


class DefaultNotificationSettings(NotificationSettings):
    """Default implementation of notification settings"""
    def __init__(self):
        self.email_enabled = True
        self.sms_enabled = True
    
    def enable_email_notifications(self, enabled: bool) -> None:
        """Enable or disable email notifications"""
        self.email_enabled = enabled
    
    def enable_sms_notifications(self, enabled: bool) -> None:
        """Enable or disable SMS notifications"""
        self.sms_enabled = enabled
    
    def is_email_enabled(self) -> bool:
        """Check if email notifications are enabled"""
        return self.email_enabled
    
    def is_sms_enabled(self) -> bool:
        """Check if SMS notifications are enabled"""
        return self.sms_enabled


class NotificationService:
    """
    Refactored NotificationService that follows SOLID principles by delegating
    responsibilities to appropriate components.
    """
    
    def __init__(
        self,
        notification_sender: Optional[NotificationSender] = None,
        order_notifier: Optional[OrderNotifier] = None,
        marketing_notifier: Optional[MarketingNotifier] = None,
        customer_notifier: Optional[CustomerNotifier] = None,
        supplier_notifier: Optional[SupplierNotifier] = None,
        notification_logger: Optional[NotificationLogger] = None,
        notification_settings: Optional[NotificationSettings] = None
    ):
        # Use dependency injection for all components
        self.notification_sender = notification_sender or DefaultNotificationSender()
        self.order_notifier = order_notifier or DefaultOrderNotifier(self.notification_sender)
        self.marketing_notifier = marketing_notifier or DefaultMarketingNotifier(self.notification_sender)
        self.customer_notifier = customer_notifier or DefaultCustomerNotifier(self.notification_sender)
        self.supplier_notifier = supplier_notifier or DefaultSupplierNotifier(self.notification_sender)
        self.notification_logger = notification_logger or DefaultNotificationLogger()
        self.notification_settings = notification_settings or DefaultNotificationSettings()
    
    # Order notification operations
    def send_order_confirmation(self, customer: Customer, order: Order) -> bool:
        """Send order confirmation notification"""
        if not self.notification_settings.is_email_enabled():
            return False
        return self.order_notifier.send_order_confirmation(customer, order)
    
    def send_order_status_update(self, customer: Customer, order: Order) -> bool:
        """Send order status update notification"""
        if not self.notification_settings.is_email_enabled():
            return False
        return self.order_notifier.send_order_status_update(customer, order)
    
    def send_shipping_notification(self, customer: Customer, order: Order) -> bool:
        """Send shipping notification"""
        success = False
        
        # Send email notification
        if self.notification_settings.is_email_enabled():
            success = self.order_notifier.send_shipping_notification(customer, order)
        
        # Send SMS notification if enabled and phone is available
        if self.notification_settings.is_sms_enabled() and customer.phone:
            sms_message = f"Order {order.order_id} shipped. Track: {order.tracking_number}"
            success = self.notification_sender.send_sms(customer.phone, sms_message) or success
        
        return success
    
    def send_delivery_notification(self, customer: Customer, order: Order) -> bool:
        """Send delivery notification"""
        if not self.notification_settings.is_email_enabled():
            return False
        return self.order_notifier.send_delivery_notification(customer, order)
    
    def send_cancellation_notification(self, customer: Customer, order: Order, reason: str) -> bool:
        """Send order cancellation notification"""
        if not self.notification_settings.is_email_enabled():
            return False
        return self.order_notifier.send_cancellation_notification(customer, order, reason)
    
    # Marketing notification operations
    def send_marketing_email(self, customers: List[Customer], subject: str, message: str) -> int:
        """Send marketing email to multiple customers"""
        if not self.notification_settings.is_email_enabled():
            return 0
        return self.marketing_notifier.send_marketing_email(customers, subject, message)
    
    # Customer notification operations
    def send_membership_upgrade_notification(self, customer: Customer, new_tier: str) -> bool:
        """Send membership upgrade notification"""
        if not self.notification_settings.is_email_enabled():
            return False
        return self.customer_notifier.send_membership_upgrade_notification(customer, new_tier)
    
    # Supplier notification operations
    def send_low_stock_alert(self, supplier_email: str, product_name: str, current_stock: int) -> bool:
        """Send low stock alert to supplier"""
        if not self.notification_settings.is_email_enabled():
            return False
        return self.supplier_notifier.send_low_stock_alert(supplier_email, product_name, current_stock)
    
    # Notification logging operations
    def get_notification_history(self, notification_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get notification history, optionally filtered by type"""
        return self.notification_logger.get_notification_history(notification_type)
    
    # Notification settings operations
    def enable_email_notifications(self, enabled: bool) -> None:
        """Enable or disable email notifications"""
        self.notification_settings.enable_email_notifications(enabled)
    
    def enable_sms_notifications(self, enabled: bool) -> None:
        """Enable or disable SMS notifications"""
        self.notification_settings.enable_sms_notifications(enabled)