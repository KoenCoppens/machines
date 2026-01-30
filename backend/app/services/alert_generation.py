from datetime import date, timedelta

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models


ALERT_TYPE_EXPIRING = "WARRANTY_EXPIRING"
ALERT_TYPE_EXPIRED = "WARRANTY_EXPIRED"
ALERT_TYPE_DUE = "WARRANTY_DUE"


def generate_alerts_for_today(db: Session, today: date) -> dict:
    rules = db.query(models.AlertRule).filter(models.AlertRule.enabled == True).all()  # noqa: E712
    machines = (
        db.query(models.Machine)
        .filter(models.Machine.warranty_end_date.isnot(None), models.Machine.is_deleted == False)  # noqa: E712
        .all()
    )
    created = 0
    skipped = 0
    evaluated = 0
    for rule in rules:
        for machine in machines:
            evaluated += 1
            target_date = machine.warranty_end_date + timedelta(days=rule.offset_days)
            if target_date != today:
                continue
            if rule.offset_days < 0:
                alert_type = ALERT_TYPE_EXPIRING
            elif rule.offset_days == 0:
                alert_type = ALERT_TYPE_DUE
            else:
                alert_type = ALERT_TYPE_EXPIRED
            alert = models.Alert(
                machine_id=machine.id,
                alert_type=alert_type,
                alert_date=today,
                due_date=machine.warranty_end_date,
                status="OPEN",
            )
            db.add(alert)
            try:
                db.commit()
                created += 1
            except IntegrityError:
                db.rollback()
                skipped += 1
    return {"created": created, "skipped": skipped, "evaluated": evaluated}
