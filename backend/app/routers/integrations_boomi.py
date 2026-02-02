from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.db import get_session
from app.utils.hashing import sha256_payload

router = APIRouter()


def _filter_payload(payload: Dict[str, Any], allowed: set) -> Dict[str, Any]:
    return {key: value for key, value in payload.items() if key in allowed}


def _upsert(model, payload: Dict[str, Any], db: Session):
    sync_hash = sha256_payload(payload)
    record, skipped = crud.boomi_upsert(db, model, payload, sync_hash)
    return schemas.UpsertResponse(status="upserted", id=str(record.id), skipped=skipped)


@router.post("/accounts:upsert", response_model=schemas.UpsertResponse)
def upsert_account(payload: Dict[str, Any], db: Session = Depends(get_session)):
    allowed = {
        "external_id",
        "account_number",
        "name",
        "phone",
        "email",
        "website",
        "language",
        "is_solvable",
        "billing_street",
        "billing_house_number",
        "billing_postal_code",
        "billing_city",
        "billing_country",
        "manual_override_fields",
        "last_modified",
    }
    filtered = _filter_payload(payload, allowed)
    if "external_id" not in filtered:
        raise HTTPException(status_code=400, detail="external_id is required")
    return _upsert(models.Account, filtered, db)


@router.post("/contacts:upsert", response_model=schemas.UpsertResponse)
def upsert_contact(payload: Dict[str, Any], db: Session = Depends(get_session)):
    allowed = {
        "external_id",
        "account_id",
        "first_name",
        "last_name",
        "display_name",
        "email",
        "phone",
        "role",
        "is_primary",
        "manual_override_fields",
        "last_modified",
    }
    filtered = _filter_payload(payload, allowed)
    if "external_id" not in filtered:
        raise HTTPException(status_code=400, detail="external_id is required")
    return _upsert(models.Contact, filtered, db)


@router.post("/locations:upsert", response_model=schemas.UpsertResponse)
def upsert_location(payload: Dict[str, Any], db: Session = Depends(get_session)):
    allowed = {
        "external_id",
        "account_id",
        "location_code",
        "name",
        "street",
        "house_number",
        "postal_code",
        "city",
        "country",
        "geo_lat",
        "geo_lng",
        "manual_override_fields",
        "last_modified",
    }
    filtered = _filter_payload(payload, allowed)
    if "external_id" not in filtered:
        raise HTTPException(status_code=400, detail="external_id is required")
    return _upsert(models.Location, filtered, db)


@router.post("/machines:upsert", response_model=schemas.UpsertResponse)
def upsert_machine(payload: Dict[str, Any], db: Session = Depends(get_session)):
    allowed = {
        "external_id",
        "account_id",
        "location_id",
        "machine_name",
        "machine_number",
        "status",
        "product_category",
        "family_name",
        "family_code",
        "installation_date",
        "warranty_months",
        "warranty_end_date",
        "warranty_type",
        "manual_override_fields",
        "last_modified",
    }
    filtered = _filter_payload(payload, allowed)
    if "external_id" not in filtered:
        raise HTTPException(status_code=400, detail="external_id is required")
    machine_payload = schemas.MachineBase(**filtered).dict(exclude_unset=True)
    if "last_modified" in filtered:
        machine_payload["last_modified"] = filtered["last_modified"]
    return _upsert(models.Machine, machine_payload, db)
