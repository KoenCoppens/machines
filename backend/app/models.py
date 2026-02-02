import uuid
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects import mssql
from sqlalchemy.orm import relationship

from .db import Base


class TimestampMixin:
    created_at = Column(
        mssql.DATETIMEOFFSET,
        nullable=False,
        server_default=func.sysdatetimeoffset(),
    )
    updated_at = Column(
        mssql.DATETIMEOFFSET,
        nullable=False,
        server_default=func.sysdatetimeoffset(),
        server_onupdate=func.sysdatetimeoffset(),
    )


class SoftDeleteMixin:
    is_deleted = Column(Boolean, nullable=False, server_default=text("0"))


class Account(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "accounts"

    id = Column(mssql.UNIQUEIDENTIFIER, primary_key=True, server_default=text("NEWID()"))
    account_number = Column(String(50), nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    phone = Column(String(50))
    email = Column(String(200))
    website = Column(String(200))
    language = Column(String(10))
    is_solvable = Column(Boolean, nullable=False, server_default=text("1"))
    billing_street = Column(String(200))
    billing_house_number = Column(String(50))
    billing_postal_code = Column(String(20))
    billing_city = Column(String(100))
    billing_country = Column(String(2))
    external_source = Column(String(20))
    external_id = Column(String(100))
    last_synced_at = Column(mssql.DATETIMEOFFSET)
    sync_hash = Column(String(64))
    manual_override_fields = Column(Text)

    contacts = relationship("Contact", back_populates="account", cascade="all, delete-orphan")
    locations = relationship("Location", back_populates="account", cascade="all, delete-orphan")
    machines = relationship("Machine", back_populates="account", cascade="all, delete-orphan")


class Contact(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "contacts"

    id = Column(mssql.UNIQUEIDENTIFIER, primary_key=True, server_default=text("NEWID()"))
    account_id = Column(mssql.UNIQUEIDENTIFIER, ForeignKey("accounts.id"), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    display_name = Column(String(200))
    email = Column(String(200))
    phone = Column(String(50))
    role = Column(String(100))
    is_primary = Column(Boolean, nullable=False, server_default=text("0"))
    external_source = Column(String(20))
    external_id = Column(String(100))
    last_synced_at = Column(mssql.DATETIMEOFFSET)
    sync_hash = Column(String(64))
    manual_override_fields = Column(Text)

    account = relationship("Account", back_populates="contacts")


class Location(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "locations"

    id = Column(mssql.UNIQUEIDENTIFIER, primary_key=True, server_default=text("NEWID()"))
    account_id = Column(mssql.UNIQUEIDENTIFIER, ForeignKey("accounts.id"), nullable=False)
    location_code = Column(String(50), nullable=False, unique=True)
    name = Column(String(200))
    street = Column(String(200))
    house_number = Column(String(50))
    postal_code = Column(String(20))
    city = Column(String(100))
    country = Column(String(2))
    geo_lat = Column(mssql.DECIMAL(9, 6))
    geo_lng = Column(mssql.DECIMAL(9, 6))
    external_source = Column(String(20))
    external_id = Column(String(100))
    last_synced_at = Column(mssql.DATETIMEOFFSET)
    sync_hash = Column(String(64))
    manual_override_fields = Column(Text)

    account = relationship("Account", back_populates="locations")
    machines = relationship("Machine", back_populates="location")


class Machine(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "machines"

    id = Column(mssql.UNIQUEIDENTIFIER, primary_key=True, server_default=text("NEWID()"))
    account_id = Column(mssql.UNIQUEIDENTIFIER, ForeignKey("accounts.id"), nullable=False)
    location_id = Column(mssql.UNIQUEIDENTIFIER, ForeignKey("locations.id"), nullable=True)
    machine_name = Column(String(200), nullable=False)
    machine_number = Column(String(100))
    status = Column(String(50))
    product_category = Column(String(100))
    family_name = Column(String(100))
    family_code = Column(String(50))
    installation_date = Column(Date)
    warranty_months = Column(Integer)
    warranty_end_date = Column(Date)
    warranty_type = Column(String(50))
    external_source = Column(String(20))
    external_id = Column(String(100))
    last_synced_at = Column(mssql.DATETIMEOFFSET)
    sync_hash = Column(String(64))
    manual_override_fields = Column(Text)

    account = relationship("Account", back_populates="machines")
    location = relationship("Location", back_populates="machines")
    alerts = relationship("Alert", back_populates="machine", cascade="all, delete-orphan")


class AlertRule(Base, TimestampMixin):
    __tablename__ = "alert_rules"

    id = Column(mssql.UNIQUEIDENTIFIER, primary_key=True, server_default=text("NEWID()"))
    name = Column(String(100), nullable=False)
    trigger = Column(String(50), nullable=False)
    offset_days = Column(Integer, nullable=False)
    enabled = Column(Boolean, nullable=False, server_default=text("1"))
    channels = Column(String(50))


class Alert(Base, TimestampMixin):
    __tablename__ = "alerts"
    __table_args__ = (
        UniqueConstraint("machine_id", "alert_type", "alert_date", name="uq_alerts_machine_type_date"),
    )

    id = Column(mssql.UNIQUEIDENTIFIER, primary_key=True, server_default=text("NEWID()"))
    machine_id = Column(mssql.UNIQUEIDENTIFIER, ForeignKey("machines.id"), nullable=False)
    alert_type = Column(String(50), nullable=False)
    alert_date = Column(Date, nullable=False)
    due_date = Column(Date)
    status = Column(String(20), nullable=False, server_default=text("'OPEN'"))
    snooze_until = Column(Date)
    assigned_to = Column(String(100))
    notes = Column(Text)

    machine = relationship("Machine", back_populates="alerts")


Index("ix_accounts_external_id", Account.external_id)
Index("ix_contacts_account_id", Contact.account_id)
Index("ix_locations_account_id", Location.account_id)
Index("ix_machines_account_id", Machine.account_id)
Index("ix_machines_location_id", Machine.location_id)
Index("ix_machines_machine_number", Machine.machine_number)
Index("ix_machines_warranty_end_date", Machine.warranty_end_date)
Index("ix_alerts_status", Alert.status)
Index("ix_alerts_due_date", Alert.due_date)
