from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str) or not self.value:
            raise ValueError("Email value must be a non-empty string.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.value):
            raise ValueError("Invalid email format.")