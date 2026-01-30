from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_session

router = APIRouter()


@router.get("/", response_model=List[schemas.AlertRule])
def list_rules(db: Session = Depends(get_session)):
    return crud.list_alert_rules(db)


@router.get("/{rule_id}", response_model=schemas.AlertRule)
def get_rule(rule_id: str, db: Session = Depends(get_session)):
    rule = crud.get_alert_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    return rule


@router.post("/", response_model=schemas.AlertRule)
def create_rule(payload: schemas.AlertRuleCreate, db: Session = Depends(get_session)):
    return crud.create_alert_rule(db, payload.dict())


@router.patch("/{rule_id}", response_model=schemas.AlertRule)
def update_rule(rule_id: str, payload: schemas.AlertRuleUpdate, db: Session = Depends(get_session)):
    rule = crud.get_alert_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    data = payload.dict(exclude_unset=True)
    return crud.update_alert_rule(db, rule, data)
