from pydantic import BaseModel
from datetime import datetime

class ClienteCreate(BaseModel):
    nombre: str

class BalanceUpdate(BaseModel):
    amount: float

class ClienteState(BaseModel):
    id: int
    nombre: str
    balance: float

class TimestampQuery(BaseModel):
    timestamp: datetime