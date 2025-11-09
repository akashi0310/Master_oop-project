from ecommerce_order_management.domain.value_objects.money import Money

class ProductId(str):
    pass

class SupplierId(str):
    pass

class Product:
    def __init__(self, product_id: ProductId, name: str, price: Money, quantity_available: int, category: str, weight: float, supplier_id: SupplierId):
        if not isinstance(product_id, ProductId) or not product_id:
            raise ValueError("Product ID must be a non-empty string.")
        if not isinstance(name, str) or not name:
            raise ValueError("Product name must be a non-empty string.")
        if not isinstance(price, Money) or price.amount <= 0:
            raise ValueError("Price must be a Money object with a positive amount.")
        if not isinstance(quantity_available, int) or quantity_available < 0:
            raise ValueError("Quantity available must be a non-negative integer.")
        if not isinstance(category, str) or not category:
            raise ValueError("Category must be a non-empty string.")
        if not isinstance(weight, (int, float)) or weight <= 0:
            raise ValueError("Weight must be a positive number.")
        if not isinstance(supplier_id, SupplierId) or not supplier_id:
            raise ValueError("Supplier ID must be a non-empty string.")

        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity_available = quantity_available
        self.category = category
        self.weight = weight
        self.supplier_id = supplier_id
        self.discount_eligible = True