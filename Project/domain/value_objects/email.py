from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Email:
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Email cannot be empty")
        
        # Basic email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, self.value):
            raise ValueError(f"Invalid email format: {self.value}")
    
    @property
    def domain(self) -> str:
        """Extract domain from email"""
        return self.value.split('@')[1]
    
    @property
    def local_part(self) -> str:
        """Extract local part (before @) from email"""
        return self.value.split('@')[0]
    
    def __str__(self) -> str:
        return self.value