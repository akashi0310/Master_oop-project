from .product_repository import InMemoryProductRepository
from .customer_repository import InMemoryCustomerRepository
from .order_repository import InMemoryOrderRepository
from .supplier_repository import InMemorySupplierRepository
from .promotion_repository import InMemoryPromotionRepository

__all__ = [
    'InMemoryProductRepository',
    'InMemoryCustomerRepository',
    'InMemoryOrderRepository',
    'InMemorySupplierRepository',
    'InMemoryPromotionRepository'
]