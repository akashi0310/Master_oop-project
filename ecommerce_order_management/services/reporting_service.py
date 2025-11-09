import datetime
from typing import Dict, Any, List

from ecommerce_order_management.domain.models.order import Order, OrderId
from ecommerce_order_management.domain.models.product import Product, ProductId
from ecommerce_order_management.domain.models.customer import Customer, CustomerId

class ReportingService:
    def __init__(self, orders: Dict[OrderId, Order], products: Dict[ProductId, Product], customers: Dict[CustomerId, Customer]):
        self.orders = orders
        self.products = products
        self.customers = customers

    def generate_sales_report(self, start_date: datetime.datetime, end_date: datetime.datetime) -> Dict[str, Any]:
        report = {
            'total_sales': 0.0,
            'total_orders': 0,
            'cancelled_orders': 0,
            'products_sold': {},
            'revenue_by_category': {},
            'top_customers': []
        }

        for order in self.orders.values():
            if start_date <= order.created_at <= end_date:
                if order.status != 'cancelled':
                    report['total_sales'] += order.total_price.amount
                    report['total_orders'] += 1

                    for item in order.items:
                        product = self.products.get(item.product_id)
                        if product:
                            if product.product_id not in report['products_sold']:
                                report['products_sold'][product.product_id] = 0
                            report['products_sold'][product.product_id] += item.quantity

                            if product.category not in report['revenue_by_category']:
                                report['revenue_by_category'][product.category] = 0.0
                            report['revenue_by_category'][product.category] += item.quantity * item.unit_price.amount
                else:
                    report['cancelled_orders'] += 1

        customer_spending = {}
        for customer_id, customer in self.customers.items():
            customer_spending[customer_id] = self._get_customer_lifetime_value(customer_id)

        sorted_customers = sorted(customer_spending.items(), key=lambda x: x[1], reverse=True)
        report['top_customers'] = sorted_customers[:10]

        return report

    def _get_customer_lifetime_value(self, customer_id: CustomerId) -> float:
        customer = self.customers.get(customer_id)
        if not customer:
            return 0.0

        total_value = 0.0
        for order_id in customer.order_history:
            order = self.orders.get(order_id)
            if order and order.status != 'cancelled':
                total_value += order.total_price.amount
        return total_value