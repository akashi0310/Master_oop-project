from ecommerce_order_management.domain.value_objects.email import Email


class SupplierId(str):
    pass

class Supplier:
    def __init__(self, supplier_id: SupplierId, name: str, email: str, reliability_score: float):
        if not isinstance(supplier_id, SupplierId) or not supplier_id:
            raise ValueError("Supplier ID must be a non-empty string.")
        if not isinstance(name, str) or not name:
            raise ValueError("Supplier name must be a non-empty string.")
        from ecommerce_order_management.domain.value_objects.email import Email
        if not isinstance(email, Email):
            raise ValueError("Email must be an Email object.")
        if not isinstance(reliability_score, (int, float)) or not (0 <= reliability_score <= 1):
            raise ValueError("Reliability score must be between 0 and 1.")

        self.supplier_id = supplier_id
        self.name = name
        self.email = email
        self.reliability_score = reliability_score