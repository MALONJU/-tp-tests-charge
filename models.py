# models.py
from pydantic import BaseModel, EmailStr, Field
from pydantic import field_validator
from typing import Optional
from datetime import datetime
import re

class Address(BaseModel):
    street: str = Field(..., min_length=2, max_length=100)
    city: str = Field(..., min_length=2, max_length=50)
    zip: str = Field(..., min_length=5, max_length=10)
    country: str = Field(..., min_length=2, max_length=50)

    @field_validator('zip')
    def validate_zip(cls, v):
        # Validation pour les codes postaux français (5 chiffres)
        if not re.match(r'^\d{5}$', v):
            raise ValueError('Code postal invalide. Doit contenir 5 chiffres.')
        return v

class Client(BaseModel):
    id: Optional[str] = None
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(..., description="Email valide selon RFC 5322")
    phone: str = Field(..., min_length=10, max_length=20)
    address: Address
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator('phone')
    def validate_phone(cls, v):
        # Validation pour les numéros de téléphone français
        if not re.match(r'^\+?33[1-9]\d{8}$', v):
            raise ValueError('Numéro de téléphone invalide. Format : +33XYYYYYYY')
        return v
