from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "USD"

    def __post_init__(self):
        if not isinstance(self.amount, (int, float)) or self.amount < 0:
            raise ValueError("Amount must be a non-negative number.")
        if not isinstance(self.currency, str) or not self.currency:
            raise ValueError("Currency must be a non-empty string.")

    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add money of different currencies.")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot subtract money of different currencies.")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, scalar: float) -> 'Money':
        if not isinstance(scalar, (int, float)):
            raise ValueError("Can only multiply Money by a numeric scalar.")
        return Money(self.amount * scalar, self.currency)

    def __truediv__(self, scalar: float) -> 'Money':
        if not isinstance(scalar, (int, float)) or scalar == 0:
            raise ValueError("Can only divide Money by a non-zero numeric scalar.")
        return Money(self.amount / scalar, self.currency)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other: 'Money') -> bool:
        if self.currency != other.currency:
            raise ValueError("Cannot compare money of different currencies.")
        return self.amount < other.amount

    def __le__(self, other: 'Money') -> bool:
        if self.currency != other.currency:
            raise ValueError("Cannot compare money of different currencies.")
        return self.amount <= other.amount

    def __gt__(self, other: 'Money') -> bool:
        if self.currency != other.currency:
            raise ValueError("Cannot compare money of different currencies.")
        return self.amount > other.amount

    def __ge__(self, other: 'Money') -> bool:
        if self.currency != other.currency:
            raise ValueError("Cannot compare money of different currencies.")
        return self.amount >= other.amount