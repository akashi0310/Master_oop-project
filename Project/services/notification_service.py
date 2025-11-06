from typing import List, Dict, Any, Optional
from datetime import datetime
from domain.models import Customer, Order


class NotificationService:
    def __init__(self):
        self.notification_history: List[Dict[str, Any]] = []
        self.email_enabled = True
        self.sms_enabled = True
    
    def send_order_confirmation(self, customer: Customer, order: Order) -> bool:
        """Send order confirmation notification"""
        if not self.email_enabled:
            return False
        
        message = f"Order {order.order_id} confirmed! Total: ${order.total_price.amount:.2f}"
        return self._send_email(customer.email.value, f"Order Confirmation", message)
    
    def send_order_status_update(self, customer: Customer, order: Order) -> bool:
        """Send order status update notification"""
        if not self.email_enabled:
            return False
        
        message = f"Order {order.order_id} status changed to {order.status.value}"
        return self._send_email(customer.email.value, f"Order Status Update", message)
    
    def send_shipping_notification(self, customer: Customer, order: Order) -> bool:
        """Send shipping notification"""
        success = False
        
        # Send email notification
        if self.email_enabled:
            message = f"Order {order.order_id} has been shipped! Tracking: {order.tracking_number}"
            success = self._send_email(customer.email.value, f"Order Shipped", message)
        
        # Send SMS notification if phone number is available
        if self.sms_enabled and customer.phone:
            sms_message = f"Order {order.order_id} shipped. Track: {order.tracking_number}"
            success = self._send_sms(customer.phone, sms_message) or success
        
        return success
    
    def send_delivery_notification(self, customer: Customer, order: Order) -> bool:
        """Send delivery notification"""
        if not self.email_enabled:
            return False
        
        message = f"Order {order.order_id} has been delivered! Thank you for your purchase."
        return self._send_email(customer.email.value, f"Order Delivered", message)
    
    def send_cancellation_notification(self, customer: Customer, order: Order, reason: str) -> bool:
        """Send order cancellation notification"""
        if not self.email_enabled:
            return False
        
        message = f"Order {order.order_id} has been cancelled. Reason: {reason}"
        return self._send_email(customer.email.value, f"Order Cancelled", message)
    
    def send_low_stock_alert(self, supplier_email: str, product_name: str, current_stock: int) -> bool:
        """Send low stock alert to supplier"""
        if not self.email_enabled:
            return False
        
        message = f"Low stock alert for {product_name}. Current stock: {current_stock}"
        return self._send_email(supplier_email, f"Low Stock Alert", message)
    
    def send_marketing_email(self, customers: List[Customer], subject: str, message: str) -> int:
        """Send marketing email to multiple customers"""
        if not self.email_enabled:
            return 0
        
        success_count = 0
        for customer in customers:
            if self._send_email(customer.email.value, subject, message):
                success_count += 1
        
        return success_count
    
    def send_membership_upgrade_notification(self, customer: Customer, new_tier: str) -> bool:
        """Send membership upgrade notification"""
        if not self.email_enabled:
            return False
        
        message = f"Congratulations! You've been upgraded to {new_tier} membership!"
        return self._send_email(customer.email.value, f"Membership Upgrade", message)
    
    def _send_email(self, email_address: str, subject: str, message: str) -> bool:
        """Send an email (simulated)"""
        # In a real system, this would integrate with an email service
        print(f"Email to {email_address}: {subject} - {message}")
        
        # Log the notification
        notification = {
            'type': 'email',
            'recipient': email_address,
            'subject': subject,
            'message': message,
            'timestamp': datetime.now(),
            'status': 'sent'
        }
        self.notification_history.append(notification)
        
        return True
    
    def _send_sms(self, phone_number: str, message: str) -> bool:
        """Send an SMS message (simulated)"""
        # In a real system, this would integrate with an SMS service
        print(f"SMS to {phone_number}: {message}")
        
        # Log the notification
        notification = {
            'type': 'sms',
            'recipient': phone_number,
            'message': message,
            'timestamp': datetime.now(),
            'status': 'sent'
        }
        self.notification_history.append(notification)
        
        return True
    
    def get_notification_history(self, notification_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get notification history, optionally filtered by type"""
        if notification_type:
            return [n for n in self.notification_history if n['type'] == notification_type]
        return self.notification_history.copy()
    
    def enable_email_notifications(self, enabled: bool) -> None:
        """Enable or disable email notifications"""
        self.email_enabled = enabled
    
    def enable_sms_notifications(self, enabled: bool) -> None:
        """Enable or disable SMS notifications"""
        self.sms_enabled = enabled
