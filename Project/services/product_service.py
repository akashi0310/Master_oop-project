from typing import List, Optional
from domain.models import Product, Supplier
from domain.value_objects import Money
from services.interfaces.product_service_interfaces import (
    ProductRepository, 
    ProductSearch, 
    ProductInventoryManager
)


class DefaultProductRepository(ProductRepository):
    """Default implementation of product repository"""
    def __init__(self):
        self.products: List[Product] = []
    
    def add_product(self, product: Product) -> None:
        """Add a new product to the repository"""
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
    
    def update_product(self, product: Product) -> bool:
        """Update a product in the repository"""
        existing_product = self.get_product(product.product_id)
        if existing_product:
            # Update the existing product with new information
            existing_product.name = product.name
            existing_product.price = product.price
            existing_product.quantity_available = product.quantity_available
            existing_product.category = product.category
            existing_product.weight = product.weight
            existing_product.supplier_id = product.supplier_id
            return True
        return False
    
    def remove_product(self, product_id: int) -> bool:
        """Remove a product from the repository"""
        for i, product in enumerate(self.products):
            if product.product_id == product_id:
                del self.products[i]
                return True
        return False


class DefaultProductSearch(ProductSearch):
    """Default implementation of product search"""
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def search_products(self, query: str) -> List[Product]:
        """Search products by name or category"""
        products = self.product_repository.get_all_products()
        query = query.lower()
        return [
            p for p in products 
            if query in p.name.lower() or query in p.category.lower()
        ]
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        products = self.product_repository.get_all_products()
        return [p for p in products if p.category.lower() == category.lower()]
    
    def get_products_by_supplier(self, supplier_id: int) -> List[Product]:
        """Get products by supplier"""
        products = self.product_repository.get_all_products()
        return [p for p in products if p.supplier_id == supplier_id]


class DefaultProductInventoryManager(ProductInventoryManager):
    """Default implementation of product inventory management"""
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def check_product_availability(self, product_id: int, quantity: int) -> bool:
        """Check if a product is available in requested quantity"""
        product = self.product_repository.get_product(product_id)
        if product:
            return product.has_sufficient_stock(quantity)
        return False
    
    def get_products_in_stock(self) -> List[Product]:
        """Get all products that are in stock"""
        products = self.product_repository.get_all_products()
        return [p for p in products if p.is_in_stock()]
    
    def get_out_of_stock_products(self) -> List[Product]:
        """Get all products that are out of stock"""
        products = self.product_repository.get_all_products()
        return [p for p in products if not p.is_in_stock()]
    
    def get_total_inventory_value(self) -> Money:
        """Calculate total value of all inventory"""
        products = self.product_repository.get_all_products()
        total = Money(0.0)
        for product in products:
            total = total.add(product.get_total_value())
        return total


class ProductService:
    """
    Refactored ProductService that follows SOLID principles by delegating
    responsibilities to appropriate components.
    """
    
    def __init__(
        self,
        product_repository: Optional[ProductRepository] = None,
        product_search: Optional[ProductSearch] = None,
        inventory_manager: Optional[ProductInventoryManager] = None
    ):
        # Use dependency injection for all components
        self.product_repository = product_repository or DefaultProductRepository()
        self.product_search = product_search or DefaultProductSearch(self.product_repository)
        self.inventory_manager = inventory_manager or DefaultProductInventoryManager(self.product_repository)
    
    # Product repository operations
    def add_product(self, product: Product) -> None:
        """Add a new product to the system"""
        self.product_repository.add_product(product)
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """Get a product by ID"""
        return self.product_repository.get_product(product_id)
    
    def get_all_products(self) -> List[Product]:
        """Get all products"""
        return self.product_repository.get_all_products()
    
    def update_product_price(self, product_id: int, new_price: Money) -> bool:
        """Update price of a product"""
        product = self.product_repository.get_product(product_id)
        if product:
            product.update_price(new_price)
            return self.product_repository.update_product(product)
        return False
    
    def remove_product(self, product_id: int) -> bool:
        """Remove a product from the system"""
        return self.product_repository.remove_product(product_id)
    
    # Product search operations
    def search_products(self, query: str) -> List[Product]:
        """Search products by name or category"""
        return self.product_search.search_products(query)
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        return self.product_search.get_products_by_category(category)
    
    def get_products_by_supplier(self, supplier_id: int) -> List[Product]:
        """Get products by supplier"""
        return self.product_search.get_products_by_supplier(supplier_id)
    
    # Inventory management operations
    def check_product_availability(self, product_id: int, quantity: int) -> bool:
        """Check if a product is available in requested quantity"""
        return self.inventory_manager.check_product_availability(product_id, quantity)
    
    def get_products_in_stock(self) -> List[Product]:
        """Get all products that are in stock"""
        return self.inventory_manager.get_products_in_stock()
    
    def get_out_of_stock_products(self) -> List[Product]:
        """Get all products that are out of stock"""
        return self.inventory_manager.get_out_of_stock_products()
    
    def get_total_inventory_value(self) -> Money:
        """Calculate total value of all inventory"""
        return self.inventory_manager.get_total_inventory_value()
    
    # Convenience methods that combine multiple operations
    def get_product_supplier(self, product_id: int, suppliers: List[Supplier]) -> Optional[Supplier]:
        """Get supplier for a product"""
        product = self.product_repository.get_product(product_id)
        if product:
            for supplier in suppliers:
                if supplier.supplier_id == product.supplier_id:
                    return supplier
        return None