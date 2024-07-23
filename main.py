from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Optional
from datetime import datetime
from models import SessionLocal, engine
import models, crud, schemas
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/clients", response_model=Dict)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db))->Dict:
    event = crud.create_client(db=db, client=client)
    return {"event_id": event.id}

@app.put("/clients/{client_id}/balance", response_model=Dict)
def update_balance(client_id: int, balance_update: schemas.BalanceUpdate, db: Session = Depends(get_db)):
    event = crud.update_balance(db=db, client_id=client_id, balance_update=balance_update)
    return {"event_id": event.id}

@app.delete("/clients/{client_id}", response_model=Dict)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    event = crud.delete_client(db=db, client_id=client_id)
    return {"event_id": event.id}

@app.get("/clients/{client_id}", response_model=schemas.ClientState)
def get_client(client_id: int, db: Session = Depends(get_db)):
    cliente_state = crud.get_client_state(db=db, client_id=client_id)
    if cliente_state is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return cliente_state

@app.get("/clients", response_model=schemas.ClientResponse)
def get_clients(db: Session = Depends(get_db)):
    cliente_list = crud.get_all(db=db)
    if cliente_list is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return cliente_list

@app.get("/clients/{client_id}/at", response_model=schemas.ClientState)
def get_client_at(client_id: int, timestamp: datetime = Query(...), db: Session = Depends(get_db)):
    cliente_state = crud.get_client_state(db=db, client_id=client_id, timestamp=timestamp)
    if cliente_state is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return cliente_state

@app.post("/clients/{client_id}/restore", response_model=Dict)
def restore_client_at(client_id: int, timestamp: schemas.TimestampQuery, db: Session = Depends(get_db))->Dict:
    event = crud.restore_client(db=db, client_id=client_id, timestamp=timestamp)
    return {"event_id":event.id}