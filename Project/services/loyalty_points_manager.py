from abc import ABC, abstractmethod
from typing import Protocol


class LoyaltyPointsCalculator(Protocol):
    """Protocol for calculating loyalty points multipliers"""
    def get_loyalty_points_multiplier(self) -> float:
        ...


class LoyaltyPointsManager:
    """Manages loyalty points operations for a customer"""
    
    def __init__(self, initial_points: int = 0):
        if initial_points < 0:
            raise ValueError("Initial loyalty points cannot be negative")
        self._points = initial_points
    
    @property
    def points(self) -> int:
        """Get current loyalty points"""
        return self._points
    
    @points.setter
    def points(self, value: int) -> None:
        """Set loyalty points"""
        if value < 0:
            raise ValueError("Loyalty points cannot be negative")
        self._points = value
    
    def add_points(self, points: int, calculator: LoyaltyPointsCalculator) -> None:
        """Add loyalty points with multiplier based on membership tier"""
        if points <= 0:
            raise ValueError("Points to add must be positive")
        multiplier = calculator.get_loyalty_points_multiplier()
        self._points += int(points * multiplier)
    
    def redeem_points(self, points: int) -> bool:
        """Redeem loyalty points if available"""
        if points <= 0:
            raise ValueError("Points to redeem must be positive")
        if self._points >= points:
            self._points -= points
            return True
        return False