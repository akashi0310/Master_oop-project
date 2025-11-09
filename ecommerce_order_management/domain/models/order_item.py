
from ecommerce_order_management.domain.value_objects.money import Money


class ProductId(str):
    pass

class OrderId(str):
    pass


class OrderItem:
    def __init__(self, product_id: ProductId, quantity: int, unit_price: Money):
        if not isinstance(product_id, ProductId) or not product_id:
            raise ValueError("Product ID must be a non-empty string.")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        if not isinstance(unit_price, Money) or unit_price.amount <= 0:
            raise ValueError("Unit price must be a Money object with a positive amount.")

        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.discount_applied: Money = Money(0.0)