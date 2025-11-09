from enum import Enum

class MembershipTier(str, Enum):
    STANDARD = "standard"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    SUSPENDED = "suspended"