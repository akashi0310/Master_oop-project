import datetime
from storage import database
from services.customer_service import CustomerService


class ReportingService:
    def __init__(self):
        self.analytics = CustomerService()

    def generate_sales_report(self, start_date, end_date):
        """Generate sales summary report for a date range."""
        report = {
            'total_sales': 0,
            'total_orders': 0,
            'cancelled_orders': 0,
            'products_sold': {},
            'revenue_by_category': {},
            'top_customers': []
        }

        for order in database.orders.values():
            if start_date <= order.created_at <= end_date:
                if order.status != 'cancelled':
                    report['total_sales'] += order.total_price
                    report['total_orders'] += 1

                    for item in order.items:
                        product = database.products.get(item.product_id)
                        if product:
                            report['products_sold'][product.product_id] = (
                                report['products_sold'].get(product.product_id, 0) + item.quantity
                            )
                            report['revenue_by_category'][product.category] = (
                                report['revenue_by_category'].get(product.category, 0)
                                + item.quantity * item.unit_price
                            )
                else:
                    report['cancelled_orders'] += 1

        # Top customers
        spending = {
            cid: self.analytics.get_customer_lifetime_value(cid)
            for cid in database.customers
        }
        sorted_customers = sorted(spending.items(), key=lambda x: x[1], reverse=True)
        report['top_customers'] = sorted_customers[:10]

        return report
