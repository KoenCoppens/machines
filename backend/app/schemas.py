from datetime import date, datetime
from typing import List, Optional

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field, root_validator


class AccountBase(BaseModel):
    account_number: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    language: Optional[str] = None
    is_solvable: Optional[bool] = True
    billing_street: Optional[str] = None
    billing_house_number: Optional[str] = None
    billing_postal_code: Optional[str] = None
    billing_city: Optional[str] = None
    billing_country: Optional[str] = None
    external_source: Optional[str] = None
    external_id: Optional[str] = None
    last_synced_at: Optional[datetime] = None
    sync_hash: Optional[str] = None
    manual_override_fields: Optional[str] = None


class AccountCreate(AccountBase):
    account_number: str
    name: str


class AccountUpdate(AccountBase):
    pass


class Account(AccountBase):
    id: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ContactBase(BaseModel):
    account_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    is_primary: Optional[bool] = False
    external_source: Optional[str] = None
    external_id: Optional[str] = None
    last_synced_at: Optional[datetime] = None
    sync_hash: Optional[str] = None
    manual_override_fields: Optional[str] = None


class ContactCreate(ContactBase):
    account_id: str


class ContactUpdate(ContactBase):
    pass


class Contact(ContactBase):
    id: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LocationBase(BaseModel):
    account_id: Optional[str] = None
    location_code: Optional[str] = None
    name: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    geo_lat: Optional[float] = None
    geo_lng: Optional[float] = None
    external_source: Optional[str] = None
    external_id: Optional[str] = None
    last_synced_at: Optional[datetime] = None
    sync_hash: Optional[str] = None
    manual_override_fields: Optional[str] = None


class LocationCreate(LocationBase):
    account_id: str
    location_code: str


class LocationUpdate(LocationBase):
    pass


class Location(LocationBase):
    id: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class MachineBase(BaseModel):
    account_id: Optional[str] = None
    location_id: Optional[str] = None
    machine_name: Optional[str] = None
    machine_number: Optional[str] = None
    status: Optional[str] = None
    product_category: Optional[str] = None
    family_name: Optional[str] = None
    family_code: Optional[str] = None
    installation_date: Optional[date] = None
    warranty_months: Optional[int] = Field(default=None, ge=0)
    warranty_end_date: Optional[date] = None
    warranty_type: Optional[str] = None
    external_source: Optional[str] = None
    external_id: Optional[str] = None
    last_synced_at: Optional[datetime] = None
    sync_hash: Optional[str] = None
    manual_override_fields: Optional[str] = None

    @root_validator
    def compute_warranty_end_date(cls, values):
        installation_date = values.get("installation_date")
        warranty_months = values.get("warranty_months")
        warranty_end_date = values.get("warranty_end_date")
        if not warranty_end_date and installation_date and warranty_months is not None:
            values["warranty_end_date"] = installation_date + relativedelta(months=int(warranty_months))
        if installation_date and values.get("warranty_end_date"):
            if values["warranty_end_date"] < installation_date:
                raise ValueError("warranty_end_date must be >= installation_date")
        return values


class MachineCreate(MachineBase):
    account_id: str
    machine_name: str


class MachineUpdate(MachineBase):
    pass


class Machine(MachineBase):
    id: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class AlertRuleBase(BaseModel):
    name: Optional[str] = None
    trigger: Optional[str] = None
    offset_days: Optional[int] = None
    enabled: Optional[bool] = True
    channels: Optional[str] = None


class AlertRuleCreate(AlertRuleBase):
    name: str
    trigger: str
    offset_days: int


class AlertRuleUpdate(AlertRuleBase):
    pass


class AlertRule(AlertRuleBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class AlertBase(BaseModel):
    machine_id: Optional[str] = None
    alert_type: Optional[str] = None
    alert_date: Optional[date] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    snooze_until: Optional[date] = None
    assigned_to: Optional[str] = None
    notes: Optional[str] = None


class AlertUpdate(AlertBase):
    pass


class Alert(AlertBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class AlertGenerationResult(BaseModel):
    created: int
    skipped: int
    evaluated: int


class UpsertResponse(BaseModel):
    status: str
    id: str
    skipped: bool


class AlertsInboxResponse(BaseModel):
    items: List[Alert]
    total: int
