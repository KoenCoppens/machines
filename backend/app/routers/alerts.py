from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_session

router = APIRouter()


@router.get("/", response_model=List[schemas.Alert])
def list_alerts(status: Optional[str] = None, db: Session = Depends(get_session)):
    return crud.list_alerts(db, status)


@router.get("/{alert_id}", response_model=schemas.Alert)
def get_alert(alert_id: str, db: Session = Depends(get_session)):
    alert = crud.get_alert(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.patch("/{alert_id}", response_model=schemas.Alert)
def update_alert(alert_id: str, payload: schemas.AlertUpdate, db: Session = Depends(get_session)):
    alert = crud.get_alert(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    data = payload.dict(exclude_unset=True)
    return crud.update_alert(db, alert, data)

