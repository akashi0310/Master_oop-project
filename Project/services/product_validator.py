from abc import ABC, abstractmethod


class ProductValidator(ABC):
    """Abstract base class for product validation"""
    
    @abstractmethod
    def validate_product_data(
        self,
        product_id: int,
        name: str,
        quantity_available: int,
        weight: float,
        supplier_id: int,
        category: str
    ) -> None:
        """Validate product data"""
        pass


class DefaultProductValidator(ProductValidator):
    """Default implementation of product validation"""
    
    def validate_product_data(
        self,
        product_id: int,
        name: str,
        quantity_available: int,
        weight: float,
        supplier_id: int,
        category: str
    ) -> None:
        """Validate basic product data"""
        if not name or not name.strip():
            raise ValueError("Product name cannot be empty")
        if product_id <= 0:
            raise ValueError("Product ID must be positive")
        if quantity_available < 0:
            raise ValueError("Quantity available cannot be negative")
        if weight <= 0:
            raise ValueError("Weight must be positive")
        if supplier_id <= 0:
            raise ValueError("Supplier ID must be positive")
        if not category or not category.strip():
            raise ValueError("Category cannot be empty")