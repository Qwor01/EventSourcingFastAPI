from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from models import Event, EventType
from schemas import ClientCreate, BalanceUpdate
import json
from datetime import datetime

#Master method for adding a new event
def create_event(db: Session, event_type: EventType, data: dict):
    event = Event(event_type=event_type, data=json.dumps(data), timestamp=datetime.utcnow())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

#Function for the event to create a client
def create_client(db: Session, client: ClientCreate):
    event_data = {"name": client.name}
    return create_event(db, EventType.CLIENT_CREATED, event_data)

#Function for the event modifying the balance of a client, both positive and negative values are allowed
def update_balance(db: Session, client_id: int, balance_update: BalanceUpdate):
    event_data = {"client_id": client_id, "amount": balance_update.amount}
    return create_event(db, EventType.BALANCE_UPDATED, event_data)



#Function to get all clients currenty present within the table with their respective IDs
def get_all(db:Session):
    events = db.query(Event.id, Event.data, Event.event_type).all()
    
    event_list = []
    for event_id, event_data, event_type in events:
        name = None
        if event_type == EventType.CLIENT_CREATED:
            name = json.loads(event_data).get("name")
            event_dict = {"id": event_id, "name": name}
            event_list.append(event_dict)
    
    return {"clients":event_list}

#Function to get the client's current state 
def get_client_state(db: Session, client_id: int, timestamp: datetime = None):
    if timestamp is None:
        timestamp = datetime.utcnow()

    # Buscar el último CLIENT_RESTORED para este cliente antes del timestamp
    restored_event = db.query(Event).filter(
        Event.event_type == EventType.CLIENT_RESTORED,
        Event.timestamp <= timestamp
    ).order_by(Event.timestamp.desc()).all()

    name = None
    balance = 0.0
    last_restore_time = None

    for event in restored_event:
        data = json.loads(event.data)
        if data.get("id") == client_id:
            name = data.get("name")
            balance = data.get("amount", 0.0)
            last_restore_time = event.timestamp
            break

    # Buscar todos los eventos relevantes después del último restore
    query = db.query(Event).filter(
        Event.timestamp <= timestamp,
        Event.timestamp > (last_restore_time if last_restore_time else datetime.min)
    ).order_by(Event.timestamp)

    events = query.all()

    for event in events:
        data = json.loads(event.data)

        if event.event_type == EventType.CLIENT_CREATED:
            if data.get("name") and (name is None or name == data["name"]):
                name = data["name"]

        elif event.event_type == EventType.BALANCE_UPDATED:
            if data.get("client_id") == client_id:
                balance += data["amount"]

        elif event.event_type == EventType.CLIENT_DELETED:
            if data.get("client_id") == client_id:
                name = None
                balance = 0.0

    if name is None:
        return None

    return {"id": client_id, "name": name, "balance": balance}



#Function to get the client's state at a certain time
def restore_client(db: Session, client_id: int, timestamp: datetime = None):
    query = db.query(Event).filter(
        or_(
            Event.data.contains(f'"client_id": {client_id}'),
            Event.event_type == EventType.CLIENT_CREATED
        )
    )
    if timestamp:
        query = query.filter(Event.timestamp <= timestamp)
    events = query.order_by(Event.timestamp).all()

    name = None
    balance = 0.0  # ← importante

    for event in events:
        data = json.loads(event.data)
        if event.event_type == EventType.CLIENT_CREATED:
            name = data["name"]
        elif event.event_type == EventType.BALANCE_UPDATED:
            balance += data["amount"]
        elif event.event_type == EventType.CLIENT_DELETED:
            name = None
            balance = 0.0

    if name is None:
        return None

    event_data = {"id": client_id, "name": name, "amount": balance}
    return create_event(db, EventType.CLIENT_RESTORED, event_data)