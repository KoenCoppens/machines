import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    accounts,
    alerts,
    alert_rules,
    contacts,
    integrations_boomi,
    jobs,
    locations,
    machines,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("machine-mgmt")

app = FastAPI(title="Machine Management POC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("%s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("%s %s -> %s", request.method, request.url.path, response.status_code)
    return response


app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
app.include_router(locations.router, prefix="/locations", tags=["locations"])
app.include_router(machines.router, prefix="/machines", tags=["machines"])
app.include_router(alert_rules.router, prefix="/alert_rules", tags=["alert_rules"])
app.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(integrations_boomi.router, prefix="/integrations/boomi", tags=["integrations"])
