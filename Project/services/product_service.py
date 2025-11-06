from typing import List, Optional
from domain.models import Product, Supplier
from domain.value_objects import Money


class ProductService:
    def __init__(self, product_repository=None):
        self.product_repository = product_repository
        self.products: List[Product] = []
    
    def add_product(self, product: Product) -> None:
        """Add a new product to the system"""
        if any(p.product_id == product.product_id for p in self.products):
            raise ValueError(f"Product with ID {product.product_id} already exists")
        self.products.append(product)
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """Get a product by ID"""
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
    
    def get_all_products(self) -> List[Product]:
        """Get all products"""
        return self.products.copy()
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        return [p for p in self.products if p.category.lower() == category.lower()]
    
    def get_products_by_supplier(self, supplier_id: int) -> List[Product]:
        """Get products by supplier"""
        return [p for p in self.products if p.supplier_id == supplier_id]
    
    def update_product_price(self, product_id: int, new_price: Money) -> bool:
        """Update the price of a product"""
        product = self.get_product(product_id)
        if product:
            product.update_price(new_price)
            return True
        return False
    
    def check_product_availability(self, product_id: int, quantity: int) -> bool:
        """Check if a product is available in the requested quantity"""
        product = self.get_product(product_id)
        if product:
            return product.has_sufficient_stock(quantity)
        return False
    
    def get_products_in_stock(self) -> List[Product]:
        """Get all products that are in stock"""
        return [p for p in self.products if p.is_in_stock()]
    
    def get_out_of_stock_products(self) -> List[Product]:
        """Get all products that are out of stock"""
        return [p for p in self.products if not p.is_in_stock()]
    
    def search_products(self, query: str) -> List[Product]:
        """Search products by name or category"""
        query = query.lower()
        return [
            p for p in self.products 
            if query in p.name.lower() or query in p.category.lower()
        ]
    
    def get_product_supplier(self, product_id: int, suppliers: List[Supplier]) -> Optional[Supplier]:
        """Get the supplier for a product"""
        product = self.get_product(product_id)
        if product:
            for supplier in suppliers:
                if supplier.supplier_id == product.supplier_id:
                    return supplier
        return None
    
    def remove_product(self, product_id: int) -> bool:
        """Remove a product from the system"""
        for i, product in enumerate(self.products):
            if product.product_id == product_id:
                del self.products[i]
                return True
        return False
    
    def get_total_inventory_value(self) -> Money:
        """Calculate the total value of all inventory"""
        total = Money(0.0)
        for product in self.products:
            total = total.add(product.get_total_value())
        return total
