from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from domain.models import Customer, Order, OrderItem, Product, Promotion, Supplier
from domain.enums import OrderStatus, ShippingMethod
from domain.value_objects import Money

from repositories import (
    ProductRepository,
    CustomerRepository,
    OrderRepository,
    SupplierRepository,
    PromotionRepository
)

from repositories.in_memory import (
    InMemoryProductRepository,
    InMemoryCustomerRepository,
    InMemoryOrderRepository,
    InMemorySupplierRepository,
    InMemoryPromotionRepository
)

from services import (
    ProductService,
    CustomerService,
    OrderService,
    PaymentService,
    ShippingService,
    NotificationService,
    ReportingService,
    SupplierService,
    PricingService,
    InventoryService
)


class OrderProcessor:
    """Application orchestrator that wires all dependencies and processes orders"""
    
    def __init__(
        self,
        product_repository: Optional[ProductRepository] = None,
        customer_repository: Optional[CustomerRepository] = None,
        order_repository: Optional[OrderRepository] = None,
        supplier_repository: Optional[SupplierRepository] = None,
        promotion_repository: Optional[PromotionRepository] = None
    ):
        # Initialize repositories (use provided ones or create defaults)
        self.product_repository = product_repository or InMemoryProductRepository()
        self.customer_repository = customer_repository or InMemoryCustomerRepository()
        self.order_repository = order_repository or InMemoryOrderRepository()
        self.supplier_repository = supplier_repository or InMemorySupplierRepository()
        self.promotion_repository = promotion_repository or InMemoryPromotionRepository()
        
        # Initialize services with repository dependencies
        self.inventory_service = InventoryService()
        self.pricing_service = PricingService()
        self.product_service = ProductService()
        self.customer_service = CustomerService()
        self.order_service = OrderService(self.inventory_service)
        self.payment_service = PaymentService()
        self.shipping_service = ShippingService()
        self.notification_service = NotificationService()
        self.reporting_service = ReportingService()
        self.supplier_service = SupplierService()
    
    def add_customer(self, customer_id: int, name: str, email: str, membership_tier: str,
                   phone: Optional[str] = None, address: Optional[str] = None,
                   loyalty_points: int = 0) -> bool:
        """Add a new customer to the system"""
        try:
            customer = Customer(
                customer_id=customer_id,
                name=name,
                email=email,
                membership_tier=membership_tier,
                phone=phone,
                address=address,
                loyalty_points=loyalty_points
            )
            self.customer_repository.add(customer)
            return True
        except ValueError as e:
            print(f"Error adding customer: {e}")
            return False
    
    def add_product(self, product_id: int, name: str, price: float, quantity_available: int,
                  category: str, weight: float, supplier_id: int) -> bool:
        """Add a new product to the system"""
        try:
            product = Product(
                product_id=product_id,
                name=name,
                price=price,
                quantity_available=quantity_available,
                category=category,
                weight=weight,
                supplier_id=supplier_id
            )
            self.product_repository.add(product)
            return True
        except ValueError as e:
            print(f"Error adding product: {e}")
            return False
    
    def add_supplier(self, supplier_id: int, name: str, email: str, reliability_score: float,
                    phone: Optional[str] = None, address: Optional[str] = None) -> bool:
        """Add a new supplier to the system"""
        try:
            supplier = Supplier(
                supplier_id=supplier_id,
                name=name,
                email=email,
                reliability_score=reliability_score,
                phone=phone,
                address=address
            )
            self.supplier_repository.add(supplier)
            return True
        except ValueError as e:
            print(f"Error adding supplier: {e}")
            return False
    
    def add_promotion(self, promo_id: int, code: str, discount_percent: float,
                   min_purchase: float, valid_days: int, category: str = "all") -> bool:
        """Add a new promotion to the system"""
        try:
            valid_until = datetime.now() + timedelta(days=valid_days)
            promotion = Promotion(
                promo_id=promo_id,
                code=code,
                discount_percent=discount_percent,
                min_purchase=min_purchase,
                valid_until=valid_until,
                category=category
            )
            self.promotion_repository.add(promotion)
            return True
        except ValueError as e:
            print(f"Error adding promotion: {e}")
            return False
    
    def process_order(
        self,
        customer_id: int,
        order_items: List[Dict[str, Any]],
        payment_info: Dict[str, Any],
        promo_code: Optional[str] = None,
        shipping_method: str = "standard",
        loyalty_points_to_use: int = 0
    ) -> Optional[Dict[str, Any]]:
        """
        Process a complete order with all validations and calculations
        Returns order details or None if failed
        """
        try:
            # Get customer
            customer = self.customer_repository.get_by_id(customer_id)
            if not customer:
                print(f"Customer {customer_id} not found")
                return None
            
            # Convert order items to OrderItem objects
            order_item_objects = []
            for item in order_items:
                product = self.product_repository.get_by_id(item["product_id"])
                if not product:
                    print(f"Product {item['product_id']} not found")
                    return None
                
                order_item = OrderItem(
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    unit_price=item["unit_price"],
                    weight=getattr(product, 'weight', 0.0)
                )
                order_item_objects.append(order_item)
            
            # Get all promotions
            promotions = self.promotion_repository.get_all()
            
            # Process order through service
            order = self.order_service.create_order(
                customer_id=customer_id,
                order_items=order_item_objects,
                payment_info=payment_info,
                products=self.product_repository.get_all(),
                customer=customer,
                promotions=promotions,
                promo_code=promo_code,
                shipping_method=shipping_method,
                loyalty_points_to_use=loyalty_points_to_use
            )
            
            if order:
                # Add order to repository
                self.order_repository.add(order)
                
                # Send notifications
                self.notification_service.send_order_confirmation(customer, order)
                
                # Return order details
                return {
                    "order_id": order.order_id,
                    "status": order.status.value,
                    "total": order.total_price.amount,
                    "shipping_cost": order.shipping_cost.amount,
                    "message": "Order processed successfully"
                }
            
            return None
            
        except ValueError as e:
            print(f"Error processing order: {e}")
            return None
    
    def update_order_status(self, order_id: int, new_status: str, tracking_number: Optional[str] = None) -> bool:
        """Update the status of an existing order"""
        try:
            order = self.order_repository.get_by_id(order_id)
            if not order:
                print(f"Order {order_id} not found")
                return False
            
            customer = self.customer_repository.get_by_id(order.customer_id)
            if not customer:
                print(f"Customer {order.customer_id} not found")
                return False
            
            # Update order status directly in the repository
            status_enum = OrderStatus(new_status.lower())
            order.update_status(status_enum)
            
            # Update tracking number if provided
            if tracking_number:
                order.tracking_number = tracking_number
            
            # Update order in repository
            self.order_repository.update(order)
            
            # Send notification
            self.notification_service.send_order_status_update(customer, order)
            
            # If shipped, process shipping
            if status_enum == OrderStatus.SHIPPED:
                shipment = self.shipping_service.process_order_shipment(order)
                if shipment:
                    print(f"Shipment created: {shipment['shipment_id']}")
            
            return True
            
        except ValueError as e:
            print(f"Error updating order status: {e}")
            return False
    
    def cancel_order(self, order_id: int, reason: str) -> bool:
        """Cancel an existing order"""
        try:
            order = self.order_repository.get_by_id(order_id)
            if not order:
                print(f"Order {order_id} not found")
                return False
            
            customer = self.customer_repository.get_by_id(order.customer_id)
            if not customer:
                print(f"Customer {order.customer_id} not found")
                return False
            
            # Cancel order
            success = self.order_service.cancel_order(order_id, reason)
            
            if success:
                # Send notification
                self.notification_service.send_cancellation_notification(customer, order, reason)
                
                # Restore inventory
                for item in order.items:
                    product = self.product_repository.get_by_id(item.product_id)
                    if product:
                        self.inventory_service.restock_product(product, item.quantity)
            
            return success
            
        except ValueError as e:
            print(f"Error cancelling order: {e}")
            return False
    
    def get_customer_orders(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get all orders for a customer"""
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            return []
        
        orders = self.order_repository.get_by_customer(customer_id)
        return [
            {
                "order_id": order.order_id,
                "status": order.status.value,
                "created_at": order.created_at.isoformat(),
                "total": order.total_price.amount
            }
            for order in orders
        ]
    
    def get_order(self, order_id: int) -> Optional[Dict[str, Any]]:
        """Get details of a specific order"""
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return None
        
        return {
            "order_id": order.order_id,
            "customer_id": order.customer_id,
            "status": order.status.value,
            "created_at": order.created_at.isoformat(),
            "total": order.total_price.amount,
            "shipping_cost": order.shipping_cost.amount,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price.amount
                }
                for item in order.items
            ]
        }
    
    def generate_sales_report(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Generate a sales report for a date range"""
        orders = self.order_repository.get_by_date_range(start_date, end_date)
        products = self.product_repository.get_all()
        return self.reporting_service.generate_sales_report(orders, products, start_date, end_date)
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Dict[str, Any]]:
        """Get products with stock below threshold"""
        products = self.product_repository.get_all()
        low_stock_products = self.inventory_service.get_low_stock_products(products, threshold)
        
        return [
            {
                "product_id": product.product_id,
                "name": product.name,
                "quantity": product.quantity_available,
                "category": product.category
            }
            for product in low_stock_products
        ]
    
    def upgrade_customer_membership(self, customer_id: int) -> bool:
        """Upgrade a customer's membership based on lifetime value"""
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            return False
        
        orders = self.order_repository.get_by_customer(customer_id)
        lifetime_value = self.customer_service.get_customer_lifetime_value(customer_id, orders)
        
        # Determine new tier based on lifetime value
        if lifetime_value.amount >= 1000:
            new_tier = "gold"
        elif lifetime_value.amount >= 500:
            new_tier = "silver"
        elif lifetime_value.amount >= 200:
            new_tier = "bronze"
        else:
            return True  # No upgrade needed
        
        # Upgrade customer
        from domain.enums import MembershipTier
        success = self.customer_service.upgrade_membership(customer_id, MembershipTier(new_tier))
        
        if success:
            # Send notification
            self.notification_service.send_membership_upgrade_notification(customer, new_tier)
        
        return success