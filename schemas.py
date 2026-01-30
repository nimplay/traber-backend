from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
from datetime import datetime

class BadgeBase(BaseModel):
    id: str
    name: str
    icon: str

    class Config:
        from_attributes = True

class ServiceBase(BaseModel):
    id: str
    name: str
    slug: str
    icon: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class PortfolioBase(BaseModel):
    id: Optional[str] = None
    imageUrl: str
    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    id: str
    userId: str
    userName: str
    comment: str
    rating: float
    date: str

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    id: str
    name: str
    email: str
    role: str
    image: Optional[str] = None
    location_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class ProviderUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    about: Optional[str] = None
    location_name: Optional[str] = None
    type: Optional[str] = None
    image: Optional[str] = None
    hourly_rate: Optional[Dict[str, int]] = None

class PortfolioUpdate(BaseModel):
    portfolio: List[PortfolioBase]

class UserAuth(BaseModel):
    email: str
    password: str

class UserCreate(UserAuth):
    name: str
    role: str = "client"

class UserProfile(UserBase):
    phone: Optional[str] = None
    about: Optional[str] = None
    type: Optional[str] = None
    rating: Optional[float] = 0.0
    jobs: Optional[int] = 0
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    hourly_rate: Optional[Dict[str, int]] = None
    badges: List[BadgeBase] = []
    portfolio: List[PortfolioBase] = []
    reviews: List[ReviewBase] = []

class JobRequestBase(BaseModel):
    id: Optional[str] = None
    clientId: str
    providerId: Optional[str] = None
    title: str
    description: str
    type: str
    budget_min: float
    budget_max: float
    latitude: float
    longitude: float
    request_type: str = "open"
    status: str = "pending"
    images: Optional[List[str]] = None
    candidates: Optional[List[str]] = []
    milestones: Optional[List[dict]] = []
    proposal_status: Optional[str] = "none"
    budget_final: Optional[float] = None
    createdAt: Optional[datetime] = None

    class Config:
        from_attributes = True

class JobRequestCreate(BaseModel):
    title: str
    description: str
    type: str
    budget_min: float
    budget_max: float
    latitude: float
    longitude: float
    request_type: str = "open"
    images: Optional[List[str]] = None
    providerId: Optional[str] = None

class JobRequestResponse(JobRequestBase):
    client: Optional[UserBase] = None
    provider: Optional[UserBase] = None

class ProposalUpdate(BaseModel):
    milestones: List[dict]
    budget_final: float
    proposal_status: str
