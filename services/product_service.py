
from storage import database
from models.product import Product
from services.inventory_service import log_inventory_change

class ProductService:
    @staticmethod
    def add_product(product_id, name, price, quantity, category, weight, supplier_id):
        database.products[product_id] = Product(product_id, name, price, quantity, category, weight, supplier_id)
        log_inventory_change(product_id, quantity, "initial_stock")

    @staticmethod
    def get_product(product_id):
        return database.products.get(product_id)

    def restock_product(self, product_id, quantity, supplier_id=None):
        """Restock a product and log the inventory change."""
        product = database.products.get(product_id)
        if not product:
            print("Product not found")
            return False

        # Verify supplier if provided
        if supplier_id and product.supplier_id != supplier_id:
            print("Supplier mismatch")
            return False

        product.quantity_available += quantity
        log_inventory_change(product_id, quantity, "restock")
        print(f"Restocked {product.name} by {quantity}. New stock: {product.quantity_available}")
        return True

    def update_product_price(self, product_id, new_price):
        """Update a product's price and record the change."""
        product = database.products.get(product_id)
        if not product:
            print("Product not found")
            return False

        old_price = product.price
        product.price = new_price
        print(f"Updated {product.name} price from ${old_price:.2f} to ${new_price:.2f}")
        return True

    def get_low_stock_products(self, threshold=10):
        """Return a list of products below the stock threshold."""
        low_stock = [
            p for p in database.products.values()
            if p.quantity_available <= threshold
        ]
        return low_stock
