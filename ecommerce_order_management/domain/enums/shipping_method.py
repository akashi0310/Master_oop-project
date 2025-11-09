from enum import Enum

class ShippingMethod(str, Enum):
    STANDARD = "standard"
    EXPRESS = "express"
    OVERNIGHT = "overnight"