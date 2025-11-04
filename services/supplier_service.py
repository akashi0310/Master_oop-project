from storage import database
from models.supplier import Supplier

class SupplierService:
    @staticmethod
    def add_supplier(supplier_id, name, email, reliability):
        database.suppliers[supplier_id] = Supplier(supplier_id, name, email, reliability)

    @staticmethod
    def get_supplier(supplier_id):
        return database.suppliers.get(supplier_id)
