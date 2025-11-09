from dataclasses import dataclass

@dataclass(frozen=True)
class Address:
    street: str
    city: str
    state: str
    zip_code: str
    country: str

    def __post_init__(self):
        if not all(isinstance(arg, str) and arg for arg in [self.street, self.city, self.state, self.zip_code, self.country]):
            raise ValueError("All address components must be non-empty strings.")