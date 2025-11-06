# Lazy imports to avoid circular dependencies
def __getattr__(name):
    if name == 'ProductService':
        from .product_service import ProductService
        return ProductService
    elif name == 'CustomerService':
        from .customer_service import CustomerService
        return CustomerService
    elif name == 'InventoryService':
        from .inventory_service import InventoryService
        return InventoryService
    elif name == 'PricingService':
        from .pricing.pricing_service import PricingService
        return PricingService
    elif name == 'OrderService':
        from .order_service import OrderService
        return OrderService
    elif name == 'PaymentService':
        from .payment_service import PaymentService
        return PaymentService
    elif name == 'ShippingService':
        from .shipping_service import ShippingService
        return ShippingService
    elif name == 'NotificationService':
        from .notification_service import NotificationService
        return NotificationService
    elif name == 'ReportingService':
        from .reporting_service import ReportingService
        return ReportingService
    elif name == 'SupplierService':
        from .supplier_service import SupplierService
        return SupplierService
    elif name == 'LoyaltyPointsManager':
        from .loyalty_points_manager import LoyaltyPointsManager
        return LoyaltyPointsManager
    elif name == 'MembershipManager':
        from .membership_manager import MembershipManager
        return MembershipManager
    elif name == 'OrderHistoryManager':
        from .order_history_manager import OrderHistoryManager
        return OrderHistoryManager
    elif name == 'DefaultCustomerValidator':
        from .customer_validator import DefaultCustomerValidator
        return DefaultCustomerValidator
    else:
        raise AttributeError(f"module 'services' has no attribute '{name}'")

__all__ = [
    'ProductService',
    'CustomerService',
    'InventoryService',
    'PricingService',
    'OrderService',
    'PaymentService',
    'ShippingService',
    'NotificationService',
    'ReportingService',
    'SupplierService',
    'LoyaltyPointsManager',
    'MembershipManager',
    'OrderHistoryManager',
    'DefaultCustomerValidator'
]