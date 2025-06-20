# schemas.py
from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class IdentifyRequest(BaseModel):
    email: Optional[EmailStr] = None
    phoneNumber: Optional[str] = None

class IdentifyResponse(BaseModel):
    primaryContactId: int
    emails: List[str]
    phoneNumbers: List[str]
    secondaryContactIds: List[int]

