from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_session

router = APIRouter()


@router.get("/", response_model=List[schemas.Machine])
def list_machines(account_id: Optional[str] = None, db: Session = Depends(get_session)):
    return crud.list_machines(db, account_id)


@router.get("/{machine_id}", response_model=schemas.Machine)
def get_machine(machine_id: str, db: Session = Depends(get_session)):
    machine = crud.get_machine(db, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine


@router.post("/", response_model=schemas.Machine)
def create_machine(payload: schemas.MachineCreate, db: Session = Depends(get_session)):
    return crud.create_machine(db, payload.dict())


@router.patch("/{machine_id}", response_model=schemas.Machine)
def update_machine(machine_id: str, payload: schemas.MachineUpdate, db: Session = Depends(get_session)):
    machine = crud.get_machine(db, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    data = payload.dict(exclude_unset=True)
    return crud.update_machine(db, machine, data)
