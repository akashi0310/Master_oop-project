#!/usr/bin/env python3
"""
Demo usage of the refactored OOP order system.
This demonstrates the new architecture with proper separation of concerns,
dependency injection, and repository pattern.
"""

from datetime import datetime, timedelta
from typing import Dict, Any

from application.order_processor import OrderProcessor
from domain.models import OrderItem
from domain.value_objects import Money


def main():
    """Main function to demonstrate the refactored order system"""
    print("=" * 60)
    print("E-Commerce Refactored System Demo")
    print("=" * 60)
    
    # Initialize the order processor with all dependencies
    processor = OrderProcessor()
    
    # Setup suppliers
    print("\n1. Setting up suppliers...")
    processor.add_supplier(
        supplier_id=1,
        name="TechDistributor Inc",
        email="orders@techdist.com",
        reliability_score=4.5
    )
    processor.add_supplier(
        supplier_id=2,
        name="ElectroSupply Co",
        email="sales@electro.com",
        reliability_score=4.2
    )
    processor.add_supplier(
        supplier_id=3,
        name="GadgetWholesale",
        email="info@gadgetwholesale.com",
        reliability_score=4.8
    )
    
    # Setup products
    print("\n2. Adding products to inventory...")
    processor.add_product(
        product_id=1,
        name="Laptop Pro 15",
        price=999.99,
        quantity_available=15,
        category="Electronics",
        weight=2.5,
        supplier_id=1
    )
    processor.add_product(
        product_id=2,
        name="Wireless Mouse",
        price=29.99,
        quantity_available=50,
        category="Electronics",
        weight=0.2,
        supplier_id=2
    )
    processor.add_product(
        product_id=3,
        name="Mechanical Keyboard",
        price=79.99,
        quantity_available=30,
        category="Electronics",
        weight=1.0,
        supplier_id=2
    )
    processor.add_product(
        product_id=4,
        name="4K Monitor",
        price=299.99,
        quantity_available=20,
        category="Electronics",
        weight=5.0,
        supplier_id=1
    )
    processor.add_product(
        product_id=5,
        name="USB-C Hub",
        price=49.99,
        quantity_available=40,
        category="Electronics",
        weight=0.3,
        supplier_id=3
    )
    processor.add_product(
        product_id=6,
        name="Laptop Bag",
        price=39.99,
        quantity_available=25,
        category="Accessories",
        weight=0.8,
        supplier_id=3
    )
    processor.add_product(
        product_id=7,
        name="Desk Lamp",
        price=34.99,
        quantity_available=35,
        category="Accessories",
        weight=1.2,
        supplier_id=3
    )
    processor.add_product(
        product_id=8,
        name="Ergonomic Chair",
        price=299.99,
        quantity_available=10,
        category="Furniture",
        weight=15.0,
        supplier_id=1
    )
    processor.add_product(
        product_id=9,
        name="Standing Desk",
        price=499.99,
        quantity_available=8,
        category="Furniture",
        weight=25.0,
        supplier_id=1
    )
    processor.add_product(
        product_id=10,
        name="Webcam HD",
        price=79.99,
        quantity_available=45,
        category="Electronics",
        weight=0.4,
        supplier_id=2
    )
    
    # Setup customers
    print("\n3. Creating customer accounts...")
    processor.add_customer(
        customer_id=101,
        name="Alice Smith",
        email="alice@email.com",
        membership_tier="gold",
        phone="555-0101",
        address="123 Main St, San Francisco CA 94102",
        loyalty_points=100
    )
    processor.add_customer(
        customer_id=102,
        name="Bob Jones",
        email="bob@email.com",
        membership_tier="silver",
        phone="555-0102",
        address="456 Oak Ave, New York NY 10001",
        loyalty_points=50
    )
    processor.add_customer(
        customer_id=103,
        name="Charlie Brown",
        email="charlie@email.com",
        membership_tier="standard",
        phone="555-0103",
        address="789 Pine Rd, Dallas TX 75001",
        loyalty_points=0
    )
    processor.add_customer(
        customer_id=104,
        name="Diana Prince",
        email="diana@email.com",
        membership_tier="bronze",
        phone="555-0104",
        address="321 Elm St, Beverly Hills CA 90210",
        loyalty_points=25
    )
    processor.add_customer(
        customer_id=105,
        name="Eve Wilson",
        email="eve@email.com",
        membership_tier="standard",
        phone="555-0105",
        address="654 Maple Dr, Albany NY 10002",
        loyalty_points=0
    )
    
    # Add some promotions
    print("\n4. Setting up promotions...")
    processor.add_promotion(
        promo_id=1,
        code="SAVE15",
        discount_percent=15,
        min_purchase=100,
        valid_days=30,
        category="Electronics"
    )
    processor.add_promotion(
        promo_id=2,
        code="WELCOME10",
        discount_percent=10,
        min_purchase=0,
        valid_days=60,
        category="all"
    )
    
    # Create first order
    print("\n5. Processing first order (Gold member, with promo code)...")
    items1 = [
        {"product_id": 1, "quantity": 1, "unit_price": 999.99},
        {"product_id": 2, "quantity": 2, "unit_price": 29.99},
        {"product_id": 5, "quantity": 1, "unit_price": 49.99}
    ]
    payment1 = {
        "valid": True, 
        "type": "credit_card", 
        "card_number": "1234567890123456", 
        "amount": 1000
    }
    order1 = processor.process_order(
        customer_id=101,
        order_items=items1,
        payment_info=payment1,
        promo_code="SAVE15",
        shipping_method='express'
    )
    if order1:
        print(f"+ Order {order1['order_id']} created successfully!")
        print(f"  Total: ${order1['total']:.2f} (includes ${order1['shipping_cost']:.2f} shipping)")
        print(f"  Status: {order1['status']}")
    
    # Create second order
    print("\n6. Processing second order (Standard member, bulk purchase)...")
    items2 = [
        {"product_id": 3, "quantity": 5, "unit_price": 79.99},
        {"product_id": 10, "quantity": 3, "unit_price": 79.99}
    ]
    payment2 = {
        "valid": True, 
        "type": "paypal", 
        "email": "charlie@email.com", 
        "amount": 700
    }
    order2 = processor.process_order(
        customer_id=103,
        order_items=items2,
        payment_info=payment2,
        shipping_method='standard'
    )
    if order2:
        print(f"+ Order {order2['order_id']} created successfully!")
        print(f"  Total: ${order2['total']:.2f}")
    
    # Create third order
    print("\n7. Processing third order (Bronze member, furniture)...")
    items3 = [
        {"product_id": 8, "quantity": 1, "unit_price": 299.99},
        {"product_id": 7, "quantity": 2, "unit_price": 34.99}
    ]
    payment3 = {
        "valid": True, 
        "type": "credit_card", 
        "card_number": "9876543210987654", 
        "amount": 400
    }
    order3 = processor.process_order(
        customer_id=104,
        order_items=items3,
        payment_info=payment3,
        shipping_method='standard'
    )
    if order3:
        print(f"+ Order {order3['order_id']} created successfully!")
    
    # Update order status
    print("\n8. Shipping an order...")
    if order1:
        updated = processor.update_order_status(order1['order_id'], 'shipped')
        if updated:
            print(f"+ Order {order1['order_id']} marked as shipped")
    
    # Check low stock
    print("\n9. Checking inventory status...")
    low_stock = processor.get_low_stock_products(15)
    if low_stock:
        print(f"! Found {len(low_stock)} products with low stock:")
        for product in low_stock[:3]:
            print(f"  - {product['name']}: {product['quantity']} units")
    
    # Generate sales report
    print("\n10. Generating sales report...")
    start = datetime.now() - timedelta(days=1)
    end = datetime.now() + timedelta(days=1)
    report = processor.generate_sales_report(start, end)
    if report:
        print(f"Total Sales: ${report['total_sales']:.2f}")
        print(f"Total Orders: {report['total_orders']}")
        print("Revenue by Category:")
        for category, revenue in report['revenue_by_category'].items():
            print(f"  {category}: ${revenue:.2f}")
    
    # Check customer orders
    print("\n11. Customer order history...")
    for cust_id in [101, 102, 103, 104]:
        orders = processor.get_customer_orders(cust_id)
        if orders:
            print(f"Customer {cust_id} has {len(orders)} orders")
    
    # Upgrade customer membership
    print("\n12. Upgrading customer memberships...")
    for cust_id in [101, 102, 103, 104]:
        upgraded = processor.upgrade_customer_membership(cust_id)
        if upgraded:
            print(f"  Customer {cust_id} membership upgraded")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()