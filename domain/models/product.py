class Product:
    def __init__(self, product_id, name, price, quantity_available, category, weight, supplier_id):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity_available = quantity_available
        self.category = category
        self.weight = weight
        self.supplier_id = supplier_id
        self.discount_eligible = True

    def __repr__(self):
        return f"<Product {self.name} (${self.price})>"
