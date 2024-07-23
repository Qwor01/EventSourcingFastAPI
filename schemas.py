from pydantic import BaseModel
from datetime import datetime
from typing import List

#Data Schemas to be used by the CRUD methods
class ClientCreate(BaseModel):
    name: str

class BalanceUpdate(BaseModel):
    amount: float

class ClientState(BaseModel):
    id: int
    name: str
    balance: float

class TimestampQuery(BaseModel):
    timestamp: datetime
    
class ClientId(BaseModel):
    id: int
    name: str
    
class ClientResponse(BaseModel):
    clients: List[ClientId]