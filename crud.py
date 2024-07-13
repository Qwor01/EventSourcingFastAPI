from sqlalchemy.orm import Session
from models import Event, EventType
from schemas import ClienteCreate, BalanceUpdate
import json
from datetime import datetime

def create_event(db: Session, event_type: EventType, data: dict):
    event = Event(event_type=event_type, data=json.dumps(data), timestamp=datetime.utcnow())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def create_cliente(db: Session, cliente: ClienteCreate):
    event_data = {"nombre": cliente.nombre}
    return create_event(db, EventType.CLIENT_CREATED, event_data)

def update_balance(db: Session, cliente_id: int, balance_update: BalanceUpdate):
    event_data = {"cliente_id": cliente_id, "amount": balance_update.amount}
    return create_event(db, EventType.BALANCE_UPDATED, event_data)

def delete_cliente(db: Session, cliente_id: int):
    event_data = {"cliente_id": cliente_id}
    return create_event(db, EventType.CLIENT_DELETED, event_data)

def get_cliente_state(db: Session, cliente_id: int, timestamp: datetime = None):
    query = db.query(Event).filter(Event.data.contains(f'"cliente_id": {cliente_id}') | Event.event_type == EventType.CLIENT_CREATED)
    if timestamp:
        query = query.filter(Event.timestamp <= timestamp)
    events = query.order_by(Event.timestamp).all()

    nombre = None
    balance = 0.0

    for event in events:
        data = json.loads(event.data)
        if event.event_type == EventType.CLIENT_CREATED:
            nombre = data["nombre"]
        elif event.event_type == EventType.BALANCE_UPDATED:
            balance += data["amount"]
        elif event.event_type == EventType.CLIENT_DELETED:
            nombre = None
            balance = 0.0

    if nombre is None:
        return None

    return {"id": cliente_id, "nombre": nombre, "balance": balance}

def restore_client(db: Session, cliente_id: int, timestamp: datetime = None):
    query = db.query(Event).filter(Event.data.contains(f'"cliente_id": {cliente_id}') | Event.event_type == EventType.CLIENT_CREATED)
    if timestamp:
        query = query.filter(Event.timestamp <= timestamp)
    events = query.order_by(Event.timestamp).all()

    for event in events:
        data = json.loads(event.data)
        if event.event_type == EventType.CLIENT_CREATED:
            nombre = data["nombre"]
        elif event.event_type == EventType.BALANCE_UPDATED:
            balance += data["amount"]
        elif event.event_type == EventType.CLIENT_DELETED:
            nombre = None
            balance = 0.0
            
    if nombre is None:
        return None
    
    event_data = {"cliente_id": cliente_id, "nombre": nombre,"amount": balance}
    return create_event(db, EventType.CLIENT_RESTORED, event_data)