from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_session

router = APIRouter()


@router.get("/", response_model=List[schemas.Contact])
def list_contacts(account_id: Optional[str] = None, db: Session = Depends(get_session)):
    return crud.list_contacts(db, account_id)


@router.get("/{contact_id}", response_model=schemas.Contact)
def get_contact(contact_id: str, db: Session = Depends(get_session)):
    contact = crud.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.post("/", response_model=schemas.Contact)
def create_contact(payload: schemas.ContactCreate, db: Session = Depends(get_session)):
    return crud.create_contact(db, payload.dict())


@router.patch("/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: str, payload: schemas.ContactUpdate, db: Session = Depends(get_session)):
    contact = crud.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    data = payload.dict(exclude_unset=True)
    return crud.update_contact(db, contact, data)
