"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column("id", mssql.UNIQUEIDENTIFIER, server_default=sa.text("NEWID()"), primary_key=True),
        sa.Column("account_number", sa.String(length=50), nullable=False, unique=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("phone", sa.String(length=50)),
        sa.Column("email", sa.String(length=200)),
        sa.Column("website", sa.String(length=200)),
        sa.Column("language", sa.String(length=10)),
        sa.Column("is_solvable", sa.Boolean(), server_default=sa.text("1"), nullable=False),
        sa.Column("billing_street", sa.String(length=200)),
        sa.Column("billing_house_number", sa.String(length=50)),
        sa.Column("billing_postal_code", sa.String(length=20)),
        sa.Column("billing_city", sa.String(length=100)),
        sa.Column("billing_country", sa.String(length=2)),
        sa.Column("external_source", sa.String(length=20)),
        sa.Column("external_id", sa.String(length=100)),
        sa.Column("last_synced_at", mssql.DATETIMEOFFSET),
        sa.Column("sync_hash", sa.String(length=64)),
        sa.Column("manual_override_fields", sa.Text()),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", mssql.DATETIMEOFFSET, server_default=sa.text("SYSDATETIMEOFFSET()"), nullable=False),
        sa.Column("updated_at", mssql.DATETIMEOFFSET, server_default=sa.text("SYSDATETIMEOFFSET()"), nullable=False),
    )
    op.create_index("ix_accounts_external_id", "accounts", ["external_id"])

    op.create_table(
        "contacts",
        sa.Column("id", mssql.UNIQUEIDENTIFIER, server_default=sa.text("NEWID()"), primary_key=True),
        sa.Column("account_id", mssql.UNIQUEIDENTIFIER, sa.ForeignKey("accounts.id"), nullable=False),
        sa.Column("first_name", sa.String(length=100)),
        sa.Column("last_name", sa.String(length=100)),
        sa.Column("display_name", sa.String(length=200)),
        sa.Column("email", sa.String(length=200)),
        sa.Column("phone", sa.String(length=50)),
        sa.Column("role", sa.String(length=100)),
        sa.Column("is_primary", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("external_source", sa.String(length=20)),
        sa.Column("external_id", sa.String(length=100)),
        sa.Column("last_synced_at", mssql.DATETIMEOFFSET),
        sa.Column("sync_hash", sa.String(length=64)),
        sa.Column("manual_override_fields", sa.Text()),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", mssql.DATETIMEOFFSET, server_default=sa.text("SYSDATETIMEOFFSET()"), nullable=False),
        sa.Column("updated_at", mssql.DATETIMEOFFSET, server_default=sa.text("SYSDATETIMEOFFSET()"), nullable=False),
    )
    op.create_index("ix_contacts_account_id", "contacts", ["account_id"])

    op.create_table(
        "locations",
        sa.Column("id", mssql.UNIQUEIDENTIFIER, server_default=sa.text("NEWID()"), primary_key=True),
        sa.Column("account_id", mssql.UNIQUEIDENTIFIER, sa.ForeignKey("accounts.id"), nullable=False),
        sa.Column("location_code", sa.String(length=50), nullable=False, unique=True),
        sa.Column("name", sa.String(length=200)),
        sa.Column("street", sa.String(length=200)),
        sa.Column("house_number", sa.String(length=50)),
        sa.Column("postal_code", sa.String(length=20)),
        sa.Column("city", sa.String(length=100)),
        sa.Column("country", sa.String(length=2)),
        sa.Column("geo_lat", mssql.DECIMAL(9, 6)),
        sa.Column("geo_lng", mssql.DECIMAL(9, 6)),
        sa.Column("external_source", sa.String(length=20)),
        sa.Column("external_id", sa.String(length=100)),
        sa.Column("last_synced_at", mssql.DATETIMEOFFSET),
        sa.Column("sync_hash", sa.String(length=64)),
        sa.Column("manual_override_fields", sa.Text()),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", mssql.DATETIMEOFFSET, server_default=sa.text("SYSDATETIMEOFFSET()"), nullable=False),
        sa.Column("updated_at", mssql.DATETIMEOFFSET, server_default=sa.text("SYSDATETIMEOFFSET()"), nullable=False),
    )
    op.create_index("ix_locations_account_id", "locations", ["account_id"])

    op.create_table(
        "machines",
        sa.Column("id", mssql.UNIQUEIDENTIFIER, server_default=sa.text("NEWID()"), primary_key=True),
        sa.Column("account_id", mssql.UNIQUEIDENTIFIER, sa.ForeignKey("accounts.id"), nullable=False),
        sa.Column("location_id", mssql.UNIQUEIDENTIFIER, sa.ForeignKey("locations.id"), nullable=True),
        sa.Column("machine_name", sa.String(length=200), nullable=False),
        sa.Column("machine_number", sa.String(length=100)),
        sa.Column("status", sa.String(length=50)),
        sa.Column("product_category", sa.String(length=100)),
        sa.Column("family_name", sa.String(length=100)),
        sa.Column("family_code", sa.String(length=50)),
        sa.Column("installation_date", sa.Date()),
        sa.Column("warranty_months", sa.Integer()),
        sa.Column("warranty_end_date", sa.Date()),
        sa.Column("warranty_type", sa.String(length=50)),
        sa.Column("external_source", sa.String(length=20)),
        sa.Column("external_id", sa.String(length=100)),
        sa.Column("last_synced_at", mssql.DATETIMEOFFSET),
        sa.Column("sync_hash", sa.String(length=64)),
        sa.Column("manual_override_fields", sa.Text()),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", mssql.DATETIMEOFFSET, server_default=sa.text("SYSDATETIMEOFFSET()"), nullable=False),
        sa.Column("updated_at", mssql.DATETIMEOFFSET, server_default=sa.text("SYSDATETIMEOFFSET()"), nullable=False),
    )
    op.create_index("ix_machines_account_id", "machines", ["account_id"])
    op.create_index("ix_machines_location_id", "machines", ["location_id"])
    op.create_index("ix_machines_machine_number", "machines", ["machine_number"])
    op.create_index("ix_machines_warranty_end_date", "machines", ["warranty_end_date"])

    op.create_table(
        "alert_rules",
        sa.Column("id", mssql.UNIQUEIDENTIFIER, server_default=sa.text("NEWID()"), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("trigger", sa.String(length=50), nullable=False),
        sa.Column("offset_days", sa.Integer(), nullable=False),
        sa.Column("enabled", sa.Boolean(), server_default=sa.text("1"), nullable=False),
        sa.Column("channels", sa.String(length=50)),
        sa.Column("created_at", mssql.DATETIMEOFFSET, server_default=sa.text("SYSDATETIMEOFFSET()"), nullable=False),
        sa.Column("updated_at", mssql.DATETIMEOFFSET, server_default=sa.text("SYSDATETIMEOFFSET()"), nullable=False),
    )

    op.create_table(
        "alerts",
        sa.Column("id", mssql.UNIQUEIDENTIFIER, server_default=sa.text("NEWID()"), primary_key=True),
        sa.Column("machine_id", mssql.UNIQUEIDENTIFIER, sa.ForeignKey("machines.id"), nullable=False),
        sa.Column("alert_type", sa.String(length=50), nullable=False),
        sa.Column("alert_date", sa.Date(), nullable=False),
        sa.Column("due_date", sa.Date()),
        sa.Column("status", sa.String(length=20), server_default=sa.text("'OPEN'"), nullable=False),
        sa.Column("snooze_until", sa.Date()),
        sa.Column("assigned_to", sa.String(length=100)),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", mssql.DATETIMEOFFSET, server_default=sa.text("SYSDATETIMEOFFSET()"), nullable=False),
        sa.Column("updated_at", mssql.DATETIMEOFFSET, server_default=sa.text("SYSDATETIMEOFFSET()"), nullable=False),
        sa.UniqueConstraint("machine_id", "alert_type", "alert_date", name="uq_alerts_machine_type_date"),
    )
    op.create_index("ix_alerts_status", "alerts", ["status"])
    op.create_index("ix_alerts_due_date", "alerts", ["due_date"])


def downgrade() -> None:
    op.drop_index("ix_alerts_due_date", table_name="alerts")
    op.drop_index("ix_alerts_status", table_name="alerts")
    op.drop_table("alerts")
    op.drop_table("alert_rules")
    op.drop_index("ix_machines_warranty_end_date", table_name="machines")
    op.drop_index("ix_machines_machine_number", table_name="machines")
    op.drop_index("ix_machines_location_id", table_name="machines")
    op.drop_index("ix_machines_account_id", table_name="machines")
    op.drop_table("machines")
    op.drop_index("ix_locations_account_id", table_name="locations")
    op.drop_table("locations")
    op.drop_index("ix_contacts_account_id", table_name="contacts")
    op.drop_table("contacts")
    op.drop_index("ix_accounts_external_id", table_name="accounts")
    op.drop_table("accounts")
