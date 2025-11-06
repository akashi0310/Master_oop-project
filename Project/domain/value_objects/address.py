from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Address:
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"
    
    def __post_init__(self):
        if not self.street or not self.street.strip():
            raise ValueError("Street cannot be empty")
        if not self.city or not self.city.strip():
            raise ValueError("City cannot be empty")
        if not self.state or not self.state.strip():
            raise ValueError("State cannot be empty")
        if not self.zip_code or not self.zip_code.strip():
            raise ValueError("Zip code cannot be empty")
    
    @classmethod
    def from_string(cls, address_str: str) -> 'Address':
        """Create an Address from a string like '123 Main St, CA 94102'"""
        parts = address_str.split(',')
        if len(parts) < 2:
            raise ValueError("Address string must be in format 'street, city, state zip'")
        
        street = parts[0].strip()
        city_state_zip = parts[1].strip()
        
        # Split city and state+zip
        city_parts = city_state_zip.split()
        if len(city_parts) < 2:
            raise ValueError("Address string must include city, state, and zip")
        
        # Last part is zip, second to last is state, rest is city
        zip_code = city_parts[-1]
        state = city_parts[-2]
        city = ' '.join(city_parts[:-2])
        
        return cls(street, city, state, zip_code)
    
    def contains_state(self, state_code: str) -> bool:
        """Check if address contains the given state code"""
        return state_code.upper() in self.state.upper()
    
    def __str__(self) -> str:
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"