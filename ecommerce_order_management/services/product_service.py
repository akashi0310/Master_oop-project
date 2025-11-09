from ecommerce_order_management.domain.models.product import Product, ProductId, SupplierId
from typing import Dict, List

class ProductService:
    def __init__(self, products: Dict[ProductId, Product]):
        self.products = products

    def add_product(self, product_id: ProductId, name: str, price: float, quantity: int, category: str, weight: float, supplier_id: SupplierId) -> None:
        self.products[product_id] = Product(product_id, name, price, quantity, category, weight, supplier_id)
        # Inventory logging will be handled by InventoryService

    def get_product(self, product_id: ProductId) -> Product | None:
        return self.products.get(product_id)

    def update_product_price(self, product_id: ProductId, new_price: float) -> bool:
        product = self.products.get(product_id)
        if not product:
            return False
        product.price = new_price
        return True

    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        low_stock = []
        for product in self.products.values():
            if product.quantity_available <= threshold:
                low_stock.append(product)
        return low_stock