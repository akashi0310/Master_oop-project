from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from domain.models import Order, Customer, Product, OrderItem
from domain.value_objects import Money


class ReportingService:
    def __init__(self):
        pass  # No state needed for this service
    
    def generate_sales_report(
        self, 
        orders: List[Order], 
        products: List[Product], 
        start_date: datetime, 
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive sales report for a date range
        """
        if start_date > end_date:
            raise ValueError("Start date must be before end date")
        
        report = {
            'total_sales': Money(0.0),
            'total_orders': 0,
            'cancelled_orders': 0,
            'products_sold': {},
            'revenue_by_category': {},
            'top_customers': [],
            'average_order_value': Money(0.0)
        }
        
        # Filter orders by date range
        filtered_orders = [
            order for order in orders 
            if start_date <= order.created_at <= end_date
        ]
        
        # Calculate total sales and order counts
        for order in filtered_orders:
            if order.status.value != 'cancelled':
                report['total_sales'] = report['total_sales'].add(order.total_price)
                report['total_orders'] += 1
                
                # Track products sold
                for item in order.items:
                    product_id = item.product_id
                    if product_id not in report['products_sold']:
                        report['products_sold'][product_id] = 0
                    report['products_sold'][product_id] += item.quantity
                    
                    # Track revenue by category
                    product = next((p for p in products if p.product_id == product_id), None)
                    if product:
                        category = product.category
                        if category not in report['revenue_by_category']:
                            report['revenue_by_category'][category] = Money(0.0)
                        
                        item_revenue = item.unit_price.multiply(item.quantity)
                        report['revenue_by_category'][category] = report['revenue_by_category'][category].add(item_revenue)
            else:
                report['cancelled_orders'] += 1
        
        # Calculate average order value
        if report['total_orders'] > 0:
            report['average_order_value'] = Money(
                report['total_sales'].amount / report['total_orders']
            )
        
        return report
    
    def get_top_selling_products(
        self, 
        orders: List[Order], 
        products: List[Product], 
        limit: int = 10
    ) -> List[Tuple[Product, int]]:
        """
        Get top selling products by quantity
        Returns list of (product, quantity_sold) tuples
        """
        product_quantities = {}
        
        # Count quantities sold
        for order in orders:
            if order.status.value != 'cancelled':
                for item in order.items:
                    product_id = item.product_id
                    if product_id not in product_quantities:
                        product_quantities[product_id] = 0
                    product_quantities[product_id] += item.quantity
        
        # Create product lookup
        product_lookup = {p.product_id: p for p in products}
        
        # Create list of (product, quantity) tuples
        product_sales = []
        for product_id, quantity in product_quantities.items():
            product = product_lookup.get(product_id)
            if product:
                product_sales.append((product, quantity))
        
        # Sort by quantity (descending) and return top N
        product_sales.sort(key=lambda x: x[1], reverse=True)
        return product_sales[:limit]
    
    def get_revenue_by_category(
        self, 
        orders: List[Order], 
        products: List[Product]
    ) -> Dict[str, Money]:
        """Get total revenue by product category"""
        revenue_by_category = {}
        
        for order in orders:
            if order.status.value != 'cancelled':
                for item in order.items:
                    product = next((p for p in products if p.product_id == item.product_id), None)
                    if product:
                        category = product.category
                        if category not in revenue_by_category:
                            revenue_by_category[category] = Money(0.0)
                        
                        item_revenue = item.unit_price.multiply(item.quantity)
                        revenue_by_category[category] = revenue_by_category[category].add(item_revenue)
        
        return revenue_by_category
    
    def get_customer_segment_report(
        self, 
        customers: List[Customer], 
        orders: List[Order]
    ) -> Dict[str, Any]:
        """Generate a customer segmentation report"""
        segments = {
            'new': 0,      # < 30 days
            'active': 0,     # 30-90 days
            'at_risk': 0,    # 90-180 days
            'inactive': 0     # > 180 days
        }
        
        # Calculate days since last order for each customer
        now = datetime.now()
        customer_last_order = {}
        
        for order in orders:
            if order.status.value != 'cancelled':
                if order.customer_id not in customer_last_order:
                    customer_last_order[order.customer_id] = order.created_at
                elif order.created_at > customer_last_order[order.customer_id]:
                    customer_last_order[order.customer_id] = order.created_at
        
        # Segment customers based on last order date
        for customer in customers:
            if customer.customer_id in customer_last_order:
                days_since_last = (now - customer_last_order[customer.customer_id]).days
                
                if days_since_last < 30:
                    segments['new'] += 1
                elif days_since_last < 90:
                    segments['active'] += 1
                elif days_since_last < 180:
                    segments['at_risk'] += 1
                else:
                    segments['inactive'] += 1
            else:
                segments['new'] += 1  # No orders yet
        
        return segments
    
    def get_order_status_summary(self, orders: List[Order]) -> Dict[str, int]:
        """Get summary of orders by status"""
        status_counts = {}
        
        for order in orders:
            status = order.status.value
            if status not in status_counts:
                status_counts[status] = 0
            status_counts[status] += 1
        
        return status_counts
    
    def get_sales_by_date_range(
        self, 
        orders: List[Order], 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Get daily sales data for a date range"""
        if start_date > end_date:
            raise ValueError("Start date must be before end date")
        
        # Create date range
        date_range = []
        current_date = start_date.date()
        end_date_only = end_date.date()
        
        while current_date <= end_date_only:
            date_range.append(current_date)
            current_date += timedelta(days=1)
        
        # Initialize sales data for each date
        sales_data = []
        for date in date_range:
            day_start = datetime.combine(date, datetime.min.time())
            day_end = datetime.combine(date, datetime.max.time())
            
            day_orders = [
                order for order in orders 
                if day_start <= order.created_at <= day_end 
                and order.status.value != 'cancelled'
            ]
            
            day_sales = sum(order.total_price.amount for order in day_orders)
            day_count = len(day_orders)
            
            sales_data.append({
                'date': date,
                'sales': day_sales,
                'order_count': day_count
            })
        
        return sales_data
    
    def get_customer_lifetime_values(
        self, 
        customers: List[Customer], 
        orders: List[Order]
    ) -> List[Tuple[Customer, Money]]:
        """Get all customers with their lifetime values"""
        customer_values = []
        
        for customer in customers:
            total_value = Money(0.0)
            
            for order_id in customer.order_history:
                order = next((o for o in orders if o.order_id == order_id), None)
                if order and order.status.value != 'cancelled':
                    total_value = total_value.add(order.total_price)
            
            customer_values.append((customer, total_value))
        
        # Sort by lifetime value (descending)
        customer_values.sort(key=lambda x: x[1].amount, reverse=True)
        return customer_values
