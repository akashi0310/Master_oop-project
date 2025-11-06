from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "USD"
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if not self.currency or not self.currency.strip():
            raise ValueError("Currency cannot be empty")
    
    @classmethod
    def from_cents(cls, cents: int, currency: str = "USD") -> 'Money':
        """Create Money from cents"""
        return cls(cents / 100, currency)
    
    def to_cents(self) -> int:
        """Convert Money to cents"""
        return int(self.amount * 100)
    
    def add(self, other: 'Money') -> 'Money':
        """Add two Money objects"""
        if self.currency != other.currency:
            raise ValueError("Cannot add Money with different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def subtract(self, other: 'Money') -> 'Money':
        """Subtract two Money objects"""
        if self.currency != other.currency:
            raise ValueError("Cannot subtract Money with different currencies")
        if self.amount < other.amount:
            raise ValueError("Resulting amount cannot be negative")
        return Money(self.amount - other.amount, self.currency)
    
    def multiply(self, multiplier: float) -> 'Money':
        """Multiply Money by a factor"""
        if multiplier < 0:
            raise ValueError("Multiplier cannot be negative")
        return Money(self.amount * multiplier, self.currency)
    
    def apply_discount(self, discount_percent: float) -> 'Money':
        """Apply discount percentage (0-100)"""
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount percent must be between 0 and 100")
        discount_factor = discount_percent / 100
        return Money(self.amount * (1 - discount_factor), self.currency)
    
    def is_greater_than(self, other: 'Money') -> bool:
        """Check if this Money is greater than another"""
        if self.currency != other.currency:
            raise ValueError("Cannot compare Money with different currencies")
        return self.amount > other.amount
    
    def is_less_than(self, other: 'Money') -> bool:
        """Check if this Money is less than another"""
        if self.currency != other.currency:
            raise ValueError("Cannot compare Money with different currencies")
        return self.amount < other.amount
    
    def is_zero(self) -> bool:
        """Check if amount is zero"""
        return self.amount == 0
    
    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"
    
    def __format__(self, format_spec: str) -> str:
        """Support string formatting for Money objects"""
        if format_spec:
            return format(self.amount, format_spec)
        return str(self.amount)
    
    def __repr__(self) -> str:
        return f"Money({self.amount:.2f}, {self.currency})"