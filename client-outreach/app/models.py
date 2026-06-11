from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ClientTier(str, Enum):
    STONE = "Stone"
    PPCL = "PPCL"
    PRIME = "Prime"
    SPOT_ON = "Spot On Target"
    TOP_165 = "Top 165"

class ClientStatus(str, Enum):
    NEW = "new"
    PROSPECT = "prospect"
    ACTIVE = "active"
    FOLLOW_UP = "follow-up"
    INACTIVE = "inactive"
    CONVERTED = "converted"

class ClientBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    business_type: Optional[str] = None
    city: Optional[str] = None
    state: str = "CA"
    tier: ClientTier = ClientTier.STONE
    status: ClientStatus = ClientStatus.NEW
    pos_system: Optional[str] = None
    replacement_score: Optional[int] = Field(None, ge=0, le=100)
    last_contact: Optional[str] = None
    next_contact: Optional[str] = None
    notes: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    business_type: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    tier: Optional[ClientTier] = None
    status: Optional[ClientStatus] = None
    pos_system: Optional[str] = None
    replacement_score: Optional[int] = Field(None, ge=0, le=100)
    last_contact: Optional[str] = None
    next_contact: Optional[str] = None
    notes: Optional[str] = None

class Client(ClientBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class ClientList(BaseModel):
    total: int
    clients: List[Client]
    page: int
    per_page: int

class Activity(BaseModel):
    id: int
    client_id: int
    type: str
    description: Optional[str] = None
    created_at: str

class EmailQueueItem(BaseModel):
    id: int
    client_id: int
    template: str
    subject: str
    body: Optional[str] = None
    status: str
    scheduled_at: Optional[str] = None
    sent_at: Optional[str] = None
    error: Optional[str] = None

class EmailScheduleRequest(BaseModel):
    client_id: int
    template: str
    subject: str
    body: Optional[str] = None
    scheduled_at: str
