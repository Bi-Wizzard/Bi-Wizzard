from datetime import datetime

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.campaign import Campaign
from app.services.compliance_engine import ComplianceEngine
from app.services.dialer_scheduler import DialerScheduler

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.get("")
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(Campaign).all()


@router.post("")
def create_campaign(payload: dict, db: Session = Depends(get_db)):
    campaign = Campaign(
        id=payload.get("id"),
        tenant_id=payload.get("tenant_id"),
        name=payload.get("name"),
        type=payload.get("type"),
        status=payload.get("status", "DRAFT"),
        dialing_strategy=payload.get("dialing_strategy", {}),
    )
    db.add(campaign)
    db.commit()
    return campaign


@router.post("/{campaign_id}/schedule")
def schedule_campaign(
    campaign_id: str,
    payload: dict,
    db: Session = Depends(get_db),
    idempotency_key: str | None = Header(default=None),
):
    if not payload.get("idempotency_key") and not idempotency_key:
        raise HTTPException(status_code=400, detail="idempotency_key required")

    compliance = ComplianceEngine()
    scheduler = DialerScheduler()

    # Placeholder compliance check (real implementation uses DB-driven rules)
    result = compliance.check_contact_allowed(
        channel="VOICE",
        consent=True,
        is_opt_out=False,
        within_calendar=True,
        attempts_today=0,
        attempts_week=0,
        max_daily=3,
        max_weekly=10,
    )
    if not result.allowed:
        raise HTTPException(status_code=403, detail=result.reason_code)

    scheduler.schedule_contact(datetime.utcnow())
    return {"campaign_id": campaign_id, "status": "scheduled"}
