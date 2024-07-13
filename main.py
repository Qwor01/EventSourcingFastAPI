from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Optional
from datetime import datetime
from models import SessionLocal, engine
import models, crud, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/clientes/", response_model=Dict)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db))->Dict:
    event = crud.create_cliente(db=db, cliente=cliente)
    return {"event_id": event.id}

@app.put("/clientes/{cliente_id}/balance", response_model=Dict)
def update_balance(cliente_id: int, balance_update: schemas.BalanceUpdate, db: Session = Depends(get_db)):
    event = crud.update_balance(db=db, cliente_id=cliente_id, balance_update=balance_update)
    return {"event_id": event.id}

@app.delete("/clientes/{cliente_id}", response_model=Dict)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    event = crud.delete_cliente(db=db, cliente_id=cliente_id)
    return {"event_id": event.id}

@app.get("/clientes/{cliente_id}", response_model=schemas.ClienteState)
def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente_state = crud.get_cliente_state(db=db, cliente_id=cliente_id)
    if cliente_state is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente_state

@app.get("/clientes/{cliente_id}/at", response_model=schemas.ClienteState)
def get_cliente_at(cliente_id: int, timestamp: datetime = Query(...), db: Session = Depends(get_db)):
    cliente_state = crud.get_cliente_state(db=db, cliente_id=cliente_id, timestamp=timestamp)
    if cliente_state is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente_state

@app.post("/clientes/{client_id}/restore", response_model=Dict)
def restore_client_at(client_id: int, timestamp: schemas.TimestampQuery, db: Session = Depends(get_db))->Dict:
    event = crud.restore_client(db=db, client_id=client_id, timestamp=timestamp)
    return {"event_id":event.id}