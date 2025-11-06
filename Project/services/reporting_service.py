import datetime
from typing import Dict, Any, List, Optional, Tuple
from domain.models import Order, Product, Customer
from domain.value_objects import Money
from services.interfaces.reporting_service_interfaces import (
    SalesReporter, 
    ProductReporter, 
    CustomerReporter
)


class DefaultSalesReporter(SalesReporter):
    """Default implementation of sales reporting"""
    def __init__(self):
        self.orders: List[Order] = []
    
    def set_orders(self, orders: List[Order]) -> None:
        """Set the orders to report on"""
        self.orders = orders
    
    def get_sales_by_date_range(self, start_date: datetime.datetime, end_date: datetime.datetime) -> Dict[str, Any]:
        """Get sales data for a specific date range"""
        if start_date > end_date:
            raise ValueError("Start date must be before end date")
        
        filtered_orders = [
            order for order in self.orders
            if start_date <= order.order_date <= end_date
        ]
        
        total_sales = sum(order.get_total().amount for order in filtered_orders)
        total_orders = len(filtered_orders)
        
        # Calculate average order value
        avg_order_value = Money(total_sales / total_orders) if total_orders > 0 else Money(0)
        
        # Group by day
        daily_sales = {}
        for order in filtered_orders:
            date_str = order.order_date.strftime("%Y-%m-%d")
            if date_str not in daily_sales:
                daily_sales[date_str] = {"count": 0, "total": 0}
            daily_sales[date_str]["count"] += 1
            daily_sales[date_str]["total"] += order.get_total().amount
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_sales": Money(total_sales),
            "total_orders": total_orders,
            "average_order_value": avg_order_value,
            "daily_sales": daily_sales
        }
    
    def get_sales_by_product(self, product_id: Optional[int] = None) -> Dict[str, Any]:
        """Get sales data grouped by product"""
        product_sales = {}
        
        for order in self.orders:
            for item in order.items:
                pid = item.product_id
                if product_id is not None and pid != product_id:
                    continue
                
                if pid not in product_sales:
                    product_sales[pid] = {
                        "quantity": 0,
                        "revenue": 0
                    }
                
                product_sales[pid]["quantity"] += item.quantity
                product_sales[pid]["revenue"] += item.get_total().amount
        
        # Convert revenue to Money objects
        for pid in product_sales:
            product_sales[pid]["revenue"] = Money(product_sales[pid]["revenue"])
        
        return product_sales
    
    def get_top_selling_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the top-selling products by revenue"""
        if limit <= 0:
            raise ValueError("Limit must be positive")
        
        product_sales = self.get_sales_by_product()
        
        # Sort by revenue
        sorted_products = sorted(
            product_sales.items(),
            key=lambda x: x[1]["revenue"].amount,
            reverse=True
        )
        
        return [
            {
                "product_id": pid,
                "quantity": data["quantity"],
                "revenue": data["revenue"]
            }
            for pid, data in sorted_products[:limit]
        ]
    
    def get_sales_summary(self) -> Dict[str, Any]:
        """Get a summary of all sales"""
        if not self.orders:
            return {
                "total_sales": Money(0),
                "total_orders": 0,
                "average_order_value": Money(0),
                "total_customers": 0,
                "total_products_sold": 0
            }
        
        total_sales = sum(order.get_total().amount for order in self.orders)
        total_orders = len(self.orders)
        avg_order_value = Money(total_sales / total_orders)
        
        # Count unique customers
        customer_ids = {order.customer_id for order in self.orders}
        total_customers = len(customer_ids)
        
        # Count total products sold
        total_products_sold = sum(
            item.quantity for order in self.orders for item in order.items
        )
        
        return {
            "total_sales": Money(total_sales),
            "total_orders": total_orders,
            "average_order_value": avg_order_value,
            "total_customers": total_customers,
            "total_products_sold": total_products_sold
        }


class DefaultProductReporter(ProductReporter):
    """Default implementation of product reporting"""
    def __init__(self):
        self.products: List[Product] = []
        self.orders: List[Order] = []
    
    def set_products(self, products: List[Product]) -> None:
        """Set the products to report on"""
        self.products = products
    
    def set_orders(self, orders: List[Order]) -> None:
        """Set the orders to analyze for product reporting"""
        self.orders = orders
    
    def get_product_performance(self, product_id: Optional[int] = None) -> Dict[str, Any]:
        """Get performance data for products"""
        product_performance = {}
        
        # Initialize with all products
        for product in self.products:
            if product_id is not None and product.product_id != product_id:
                continue
            
            product_performance[product.product_id] = {
                "name": product.name,
                "price": product.price,
                "stock": product.stock,
                "sold": 0,
                "revenue": Money(0),
                "views": 0,  # Would be tracked in a real system
                "conversion_rate": 0.0
            }
        
        # Update with sales data
        for order in self.orders:
            for item in order.items:
                pid = item.product_id
                if pid in product_performance:
                    product_performance[pid]["sold"] += item.quantity
                    product_performance[pid]["revenue"] = product_performance[pid]["revenue"].add(item.get_total())
        
        # Calculate conversion rates (simplified)
        for pid in product_performance:
            if product_performance[pid]["views"] > 0:
                product_performance[pid]["conversion_rate"] = (
                    product_performance[pid]["sold"] / product_performance[pid]["views"]
                )
        
        return product_performance
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Dict[str, Any]]:
        """Get products with stock below the threshold"""
        if threshold < 0:
            raise ValueError("Threshold cannot be negative")
        
        low_stock = []
        
        for product in self.products:
            if product.stock < threshold:
                low_stock.append({
                    "product_id": product.product_id,
                    "name": product.name,
                    "current_stock": product.stock,
                    "threshold": threshold
                })
        
        return low_stock
    
    def get_out_of_stock_products(self) -> List[Dict[str, Any]]:
        """Get products that are out of stock"""
        out_of_stock = []
        
        for product in self.products:
            if product.stock <= 0:
                out_of_stock.append({
                    "product_id": product.product_id,
                    "name": product.name,
                    "current_stock": product.stock
                })
        
        return out_of_stock
    
    def get_product_categories_summary(self) -> Dict[str, Any]:
        """Get a summary of products by category"""
        categories = {}
        
        for product in self.products:
            category = product.category
            if category not in categories:
                categories[category] = {
                    "count": 0,
                    "total_stock": 0,
                    "total_value": Money(0)
                }
            
            categories[category]["count"] += 1
            categories[category]["total_stock"] += product.stock
            categories[category]["total_value"] = categories[category]["total_value"].add(
                Money(product.price.amount * product.stock)
            )
        
        return categories


class DefaultCustomerReporter(CustomerReporter):
    """Default implementation of customer reporting"""
    def __init__(self):
        self.customers: List[Customer] = []
        self.orders: List[Order] = []
    
    def set_customers(self, customers: List[Customer]) -> None:
        """Set the customers to report on"""
        self.customers = customers
    
    def set_orders(self, orders: List[Order]) -> None:
        """Set the orders to analyze for customer reporting"""
        self.orders = orders
    
    def get_customer_summary(self, customer_id: Optional[int] = None) -> Dict[str, Any]:
        """Get a summary of customer data"""
        customer_summary = {}
        
        # Initialize with all customers
        for customer in self.customers:
            if customer_id is not None and customer.customer_id != customer_id:
                continue
            
            customer_summary[customer.customer_id] = {
                "name": customer.name,
                "email": customer.email.value,
                "membership_tier": customer.membership_tier,
                "total_orders": 0,
                "total_spent": Money(0),
                "average_order_value": Money(0),
                "first_order_date": None,
                "last_order_date": None
            }
        
        # Update with order data
        for order in self.orders:
            cid = order.customer_id
            if cid in customer_summary:
                customer_summary[cid]["total_orders"] += 1
                customer_summary[cid]["total_spent"] = customer_summary[cid]["total_spent"].add(order.get_total())
                
                # Track first and last order dates
                if customer_summary[cid]["first_order_date"] is None or order.order_date < customer_summary[cid]["first_order_date"]:
                    customer_summary[cid]["first_order_date"] = order.order_date
                
                if customer_summary[cid]["last_order_date"] is None or order.order_date > customer_summary[cid]["last_order_date"]:
                    customer_summary[cid]["last_order_date"] = order.order_date
        
        # Calculate average order values
        for cid in customer_summary:
            if customer_summary[cid]["total_orders"] > 0:
                customer_summary[cid]["average_order_value"] = Money(
                    customer_summary[cid]["total_spent"].amount / customer_summary[cid]["total_orders"]
                )
        
        return customer_summary
    
    def get_customers_by_membership_tier(self) -> Dict[str, List[Dict[str, Any]]]:
        """Group customers by membership tier"""
        customers_by_tier = {}
        
        for customer in self.customers:
            tier = customer.membership_tier.name
            if tier not in customers_by_tier:
                customers_by_tier[tier] = []
            
            customers_by_tier[tier].append({
                "customer_id": customer.customer_id,
                "name": customer.name,
                "email": customer.email.value
            })
        
        return customers_by_tier
    
    def get_top_customers_by_spending(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the top customers by total spending"""
        if limit <= 0:
            raise ValueError("Limit must be positive")
        
        customer_summary = self.get_customer_summary()
        
        # Sort by total spent
        sorted_customers = sorted(
            customer_summary.items(),
            key=lambda x: x[1]["total_spent"].amount,
            reverse=True
        )
        
        return [
            {
                "customer_id": cid,
                "name": data["name"],
                "total_spent": data["total_spent"],
                "total_orders": data["total_orders"]
            }
            for cid, data in sorted_customers[:limit]
        ]
    
    def get_customer_segmentation(self) -> Dict[str, Any]:
        """Segment customers based on their purchasing behavior"""
        customer_summary = self.get_customer_summary()
        
        # Define segments based on total spending and order frequency
        segments = {
            "VIP": [],      # High spending, frequent orders
            "Loyal": [],    # Regular spending, regular orders
            "At Risk": [],  # Low recent activity
            "New": []       # Recent first-time customers
        }
        
        current_date = datetime.datetime.now()
        
        for cid, data in customer_summary.items():
            # Calculate days since last order
            days_since_last_order = None
            if data["last_order_date"]:
                days_since_last_order = (current_date - data["last_order_date"]).days
            
            # Segment logic (simplified)
            if data["total_spent"].amount > 1000 and data["total_orders"] > 10:
                segments["VIP"].append({"customer_id": cid, "name": data["name"]})
            elif data["total_orders"] > 5:
                segments["Loyal"].append({"customer_id": cid, "name": data["name"]})
            elif days_since_last_order and days_since_last_order > 90:
                segments["At Risk"].append({"customer_id": cid, "name": data["name"]})
            elif data["total_orders"] <= 2:
                segments["New"].append({"customer_id": cid, "name": data["name"]})
        
        return segments


class ReportingService:
    """
    Refactored ReportingService that follows SOLID principles by delegating
    responsibilities to appropriate components.
    """
    
    def __init__(
        self,
        sales_reporter: Optional[SalesReporter] = None,
        product_reporter: Optional[ProductReporter] = None,
        customer_reporter: Optional[CustomerReporter] = None
    ):
        # Use dependency injection for all components
        self.sales_reporter = sales_reporter or DefaultSalesReporter()
        self.product_reporter = product_reporter or DefaultProductReporter()
        self.customer_reporter = customer_reporter or DefaultCustomerReporter()
    
    # Data setup methods
    def set_data(self, customers: List[Customer] = None, products: List[Product] = None, orders: List[Order] = None) -> None:
        """Set the data for reporting"""
        if customers:
            self.customer_reporter.set_customers(customers)
        if products:
            self.product_reporter.set_products(products)
        if orders:
            self.sales_reporter.set_orders(orders)
            self.product_reporter.set_orders(orders)
            self.customer_reporter.set_orders(orders)
    
    # Sales reporting operations
    def get_sales_by_date_range(self, start_date: datetime.datetime, end_date: datetime.datetime) -> Dict[str, Any]:
        """Get sales data for a specific date range"""
        return self.sales_reporter.get_sales_by_date_range(start_date, end_date)
    
    def get_sales_by_product(self, product_id: Optional[int] = None) -> Dict[str, Any]:
        """Get sales data grouped by product"""
        return self.sales_reporter.get_sales_by_product(product_id)
    
    def get_top_selling_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the top-selling products by revenue"""
        return self.sales_reporter.get_top_selling_products(limit)
    
    def get_sales_summary(self) -> Dict[str, Any]:
        """Get a summary of all sales"""
        return self.sales_reporter.get_sales_summary()
    
    # Product reporting operations
    def get_product_performance(self, product_id: Optional[int] = None) -> Dict[str, Any]:
        """Get performance data for products"""
        return self.product_reporter.get_product_performance(product_id)
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Dict[str, Any]]:
        """Get products with stock below the threshold"""
        return self.product_reporter.get_low_stock_products(threshold)
    
    def get_out_of_stock_products(self) -> List[Dict[str, Any]]:
        """Get products that are out of stock"""
        return self.product_reporter.get_out_of_stock_products()
    
    def get_product_categories_summary(self) -> Dict[str, Any]:
        """Get a summary of products by category"""
        return self.product_reporter.get_product_categories_summary()
    
    # Customer reporting operations
    def get_customer_summary(self, customer_id: Optional[int] = None) -> Dict[str, Any]:
        """Get a summary of customer data"""
        return self.customer_reporter.get_customer_summary(customer_id)
    
    def get_customers_by_membership_tier(self) -> Dict[str, List[Dict[str, Any]]]:
        """Group customers by membership tier"""
        return self.customer_reporter.get_customers_by_membership_tier()
    
    def get_top_customers_by_spending(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the top customers by total spending"""
        return self.customer_reporter.get_top_customers_by_spending(limit)
    
    def get_customer_segmentation(self) -> Dict[str, Any]:
        """Segment customers based on their purchasing behavior"""
        return self.customer_reporter.get_customer_segmentation()