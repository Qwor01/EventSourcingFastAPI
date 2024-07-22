from pydantic import BaseModel
from datetime import datetime


#Data Schemas to be used by the CRUD methods
class ClienteCreate(BaseModel):
    name: str

class BalanceUpdate(BaseModel):
    amount: float

class ClienteState(BaseModel):
    id: int
    name: str
    balance: float

class TimestampQuery(BaseModel):
    timestamp: datetime