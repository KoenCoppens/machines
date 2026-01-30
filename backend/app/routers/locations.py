from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_session

router = APIRouter()


@router.get("/", response_model=List[schemas.Location])
def list_locations(account_id: Optional[str] = None, db: Session = Depends(get_session)):
    return crud.list_locations(db, account_id)


@router.get("/{location_id}", response_model=schemas.Location)
def get_location(location_id: str, db: Session = Depends(get_session)):
    location = crud.get_location(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.post("/", response_model=schemas.Location)
def create_location(payload: schemas.LocationCreate, db: Session = Depends(get_session)):
    return crud.create_location(db, payload.dict())


@router.patch("/{location_id}", response_model=schemas.Location)
def update_location(location_id: str, payload: schemas.LocationUpdate, db: Session = Depends(get_session)):
    location = crud.get_location(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    data = payload.dict(exclude_unset=True)
    return crud.update_location(db, location, data)
