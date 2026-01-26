from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.debtor import Debtor

router = APIRouter(prefix="/debtors", tags=["debtors"])


@router.get("")
def list_debtors(db: Session = Depends(get_db)):
    return db.query(Debtor).all()


@router.post("")
def create_debtor(payload: dict, db: Session = Depends(get_db)):
    debtor = Debtor(
        id=payload.get("id"),
        tenant_id=payload.get("tenant_id"),
        rut=payload.get("rut"),
        full_name=payload.get("full_name"),
        tramo_mora=payload.get("tramo_mora"),
        consent_voice=payload.get("consent_voice", True),
        consent_email=payload.get("consent_email", True),
    )
    db.add(debtor)
    db.commit()
    return debtor
