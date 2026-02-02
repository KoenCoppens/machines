# Machine Management POC (Monorepo)

This repository contains a full-stack POC for internal machine management with SQL Server, FastAPI + Alembic, and a React + Vite PWA frontend.

## Quickstart

1. Copy the env file and set a SQL Server-compliant password:
   ```bash
   cp .env.example .env
   # edit SA_PASSWORD to meet SQL Server complexity requirements
   ```
2. Start the stack:
   ```bash
   docker compose up --build
   ```
3. Run migrations (auto on backend start). If you need to run manually:
   ```bash
   docker compose exec backend alembic upgrade head
   ```
4. Seed dummy data:
   ```bash
   docker compose exec backend python -m app.services.seed
   ```
5. Open the frontend:
   - http://localhost:5173

Swagger docs are available at: http://localhost:8000/docs

## Database

The backend automatically creates the `machinemgmt` database if it does not exist. Migrations are executed on backend startup.

## Integration Upsert Examples (Boomi-like)

### Accounts
```bash
curl -X POST http://localhost:8000/integrations/boomi/accounts:upsert \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "ACC-BOOMI-1",
    "account_number": "ACC-9001",
    "name": "Boomi Antwerpen",
    "billing_city": "Antwerpen",
    "billing_country": "BE",
    "last_modified": "2024-01-20T10:00:00Z"
  }'
```

### Contacts
```bash
curl -X POST http://localhost:8000/integrations/boomi/contacts:upsert \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "CON-BOOMI-1",
    "account_id": "<account-uuid>",
    "first_name": "Marie",
    "last_name": "Dubois",
    "email": "marie.dubois@example.be",
    "last_modified": "2024-01-20T10:00:00Z"
  }'
```

### Locations
```bash
curl -X POST http://localhost:8000/integrations/boomi/locations:upsert \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "LOC-BOOMI-1",
    "account_id": "<account-uuid>",
    "location_code": "LOC-9001",
    "name": "Gent Depot",
    "city": "Gent",
    "country": "BE",
    "last_modified": "2024-01-20T10:00:00Z"
  }'
```

### Machines
```bash
curl -X POST http://localhost:8000/integrations/boomi/machines:upsert \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "MCH-BOOMI-1",
    "account_id": "<account-uuid>",
    "machine_name": "Press 5000",
    "installation_date": "2023-01-01",
    "warranty_months": 24,
    "status": "ACTIVE",
    "last_modified": "2024-01-20T10:00:00Z"
  }'
```

## Jobs

Trigger alert generation for today:
```bash
curl -X POST http://localhost:8000/jobs/generate-alerts
```

## Development Notes

- Backend connects using ODBC Driver 18 with `TrustServerCertificate=yes` for local development.
- CORS is configured for `http://localhost:5173`.
- Alerts are generated based on alert rules and machine warranty end dates.
