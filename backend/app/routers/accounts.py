from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_session

router = APIRouter()


@router.get("/", response_model=List[schemas.Account])
def list_accounts(search: Optional[str] = None, db: Session = Depends(get_session)):
    return crud.list_accounts(db, search)


@router.get("/{account_id}", response_model=schemas.Account)
def get_account(account_id: str, db: Session = Depends(get_session)):
    account = crud.get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.post("/", response_model=schemas.Account)
def create_account(payload: schemas.AccountCreate, db: Session = Depends(get_session)):
    return crud.create_account(db, payload.dict())


@router.patch("/{account_id}", response_model=schemas.Account)
def update_account(account_id: str, payload: schemas.AccountUpdate, db: Session = Depends(get_session)):
    account = crud.get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    data = payload.dict(exclude_unset=True)
    return crud.update_account(db, account, data)
