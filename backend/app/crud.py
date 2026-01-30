import json
from datetime import datetime
from typing import Any, Dict, Optional, Tuple, Type

from sqlalchemy.orm import Session

from . import models


def _parse_manual_overrides(record: Any) -> set:
    if not record or not record.manual_override_fields:
        return set()
    try:
        data = json.loads(record.manual_override_fields)
        if isinstance(data, list):
            return set(data)
    except json.JSONDecodeError:
        return set()
    return set()


def _apply_manual_overrides(record: Any, payload: Dict[str, Any]) -> Dict[str, Any]:
    overrides = _parse_manual_overrides(record)
    return {key: value for key, value in payload.items() if key not in overrides}


def _sync_metadata(payload: Dict[str, Any], sync_hash: str) -> Dict[str, Any]:
    payload["external_source"] = "BOOMI"
    payload["sync_hash"] = sync_hash
    payload["last_synced_at"] = datetime.utcnow()
    return payload


def list_accounts(db: Session, search: Optional[str] = None):
    query = db.query(models.Account).filter(models.Account.is_deleted == False)  # noqa: E712
    if search:
        query = query.filter(models.Account.name.ilike(f"%{search}%"))
    return query.order_by(models.Account.name).all()


def get_account(db: Session, account_id: str):
    return db.query(models.Account).filter(models.Account.id == account_id, models.Account.is_deleted == False).first()  # noqa: E712


def create_account(db: Session, data: Dict[str, Any]):
    account = models.Account(**data)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def update_account(db: Session, account: models.Account, data: Dict[str, Any]):
    for key, value in data.items():
        setattr(account, key, value)
    db.commit()
    db.refresh(account)
    return account


def list_contacts(db: Session, account_id: Optional[str] = None):
    query = db.query(models.Contact).filter(models.Contact.is_deleted == False)  # noqa: E712
    if account_id:
        query = query.filter(models.Contact.account_id == account_id)
    return query.order_by(models.Contact.last_name).all()


def get_contact(db: Session, contact_id: str):
    return db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.is_deleted == False).first()  # noqa: E712


def create_contact(db: Session, data: Dict[str, Any]):
    contact = models.Contact(**data)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def update_contact(db: Session, contact: models.Contact, data: Dict[str, Any]):
    for key, value in data.items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact


def list_locations(db: Session, account_id: Optional[str] = None):
    query = db.query(models.Location).filter(models.Location.is_deleted == False)  # noqa: E712
    if account_id:
        query = query.filter(models.Location.account_id == account_id)
    return query.order_by(models.Location.name).all()


def get_location(db: Session, location_id: str):
    return db.query(models.Location).filter(models.Location.id == location_id, models.Location.is_deleted == False).first()  # noqa: E712


def create_location(db: Session, data: Dict[str, Any]):
    location = models.Location(**data)
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def update_location(db: Session, location: models.Location, data: Dict[str, Any]):
    for key, value in data.items():
        setattr(location, key, value)
    db.commit()
    db.refresh(location)
    return location


def list_machines(db: Session, account_id: Optional[str] = None):
    query = db.query(models.Machine).filter(models.Machine.is_deleted == False)  # noqa: E712
    if account_id:
        query = query.filter(models.Machine.account_id == account_id)
    return query.order_by(models.Machine.machine_name).all()


def get_machine(db: Session, machine_id: str):
    return db.query(models.Machine).filter(models.Machine.id == machine_id, models.Machine.is_deleted == False).first()  # noqa: E712


def create_machine(db: Session, data: Dict[str, Any]):
    machine = models.Machine(**data)
    db.add(machine)
    db.commit()
    db.refresh(machine)
    return machine


def update_machine(db: Session, machine: models.Machine, data: Dict[str, Any]):
    for key, value in data.items():
        setattr(machine, key, value)
    db.commit()
    db.refresh(machine)
    return machine


def list_alert_rules(db: Session):
    return db.query(models.AlertRule).order_by(models.AlertRule.offset_days).all()


def get_alert_rule(db: Session, rule_id: str):
    return db.query(models.AlertRule).filter(models.AlertRule.id == rule_id).first()


def create_alert_rule(db: Session, data: Dict[str, Any]):
    rule = models.AlertRule(**data)
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


def update_alert_rule(db: Session, rule: models.AlertRule, data: Dict[str, Any]):
    for key, value in data.items():
        setattr(rule, key, value)
    db.commit()
    db.refresh(rule)
    return rule


def list_alerts(db: Session, status: Optional[str] = None):
    query = db.query(models.Alert)
    if status:
        query = query.filter(models.Alert.status == status)
    return query.order_by(models.Alert.alert_date.desc()).all()


def get_alert(db: Session, alert_id: str):
    return db.query(models.Alert).filter(models.Alert.id == alert_id).first()


def update_alert(db: Session, alert: models.Alert, data: Dict[str, Any]):
    for key, value in data.items():
        setattr(alert, key, value)
    db.commit()
    db.refresh(alert)
    return alert


def boomi_upsert(
    db: Session,
    model: Type[Any],
    payload: Dict[str, Any],
    sync_hash: str,
) -> Tuple[Any, bool]:
    external_id = payload.get("external_id")
    if not external_id:
        raise ValueError("external_id is required")
    record = db.query(model).filter(model.external_id == external_id).first()
    if record:
        if payload.get("last_modified") and record.sync_hash == sync_hash:
            return record, True
        update_payload = _apply_manual_overrides(record, payload)
        update_payload.pop("last_modified", None)
        update_payload = _sync_metadata(update_payload, sync_hash)
        for key, value in update_payload.items():
            setattr(record, key, value)
        db.commit()
        db.refresh(record)
        return record, False
    create_payload = payload.copy()
    create_payload.pop("last_modified", None)
    create_payload = _sync_metadata(create_payload, sync_hash)
    record = model(**create_payload)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record, False
