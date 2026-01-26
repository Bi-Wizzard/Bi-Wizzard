from fastapi import FastAPI

from app.api.campaigns import router as campaigns_router
from app.api.debtors import router as debtors_router
from app.api.health import router as health_router
from app.api.imports import router as imports_router
from app.api.outbound import router as outbound_router
from app.db import init_db

app = FastAPI(title="Collections Autodialer")

app.include_router(health_router)
app.include_router(campaigns_router)
app.include_router(debtors_router)
app.include_router(imports_router)
app.include_router(outbound_router)


@app.on_event("startup")
def on_startup():
    init_db()
