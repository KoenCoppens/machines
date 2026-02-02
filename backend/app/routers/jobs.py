from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_session
from app.schemas import AlertGenerationResult
from app.services.alert_generation import generate_alerts_for_today
from app.utils.time import today

router = APIRouter()


@router.post("/generate-alerts", response_model=AlertGenerationResult)
def generate_alerts(db: Session = Depends(get_session)):
    result = generate_alerts_for_today(db, today())
    return AlertGenerationResult(**result)
