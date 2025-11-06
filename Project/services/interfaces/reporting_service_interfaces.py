from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from domain.models import Order, Customer, Product, OrderItem
from domain.value_objects import Money


class SalesReporter:
    """Interface for sales reporting"""
    def generate_sales_report(
        self, 
        orders: List[Order], 
        products: List[Product], 
        start_date: datetime, 
        end_date: datetime
    ) -> Dict[str, Any]:
        """Generate a comprehensive sales report for a date range"""
        pass
    
    def get_sales_by_date_range(
        self, 
        orders: List[Order], 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Get daily sales data for a date range"""
        pass
    
    def get_order_status_summary(self, orders: List[Order]) -> Dict[str, int]:
        """Get summary of orders by status"""
        pass


class ProductReporter:
    """Interface for product reporting"""
    def get_top_selling_products(
        self, 
        orders: List[Order], 
        products: List[Product], 
        limit: int = 10
    ) -> List[Tuple[Product, int]]:
        """Get top selling products by quantity"""
        pass
    
    def get_revenue_by_category(
        self, 
        orders: List[Order], 
        products: List[Product]
    ) -> Dict[str, Money]:
        """Get total revenue by product category"""
        pass


class CustomerReporter:
    """Interface for customer reporting"""
    def get_customer_segment_report(
        self, 
        customers: List[Customer], 
        orders: List[Order]
    ) -> Dict[str, Any]:
        """Generate a customer segmentation report"""
        pass
    
    def get_customer_lifetime_values(
        self, 
        customers: List[Customer], 
        orders: List[Order]
    ) -> List[Tuple[Customer, Money]]:
        """Get all customers with their lifetime values"""
        pass