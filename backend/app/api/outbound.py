from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.outbound import OutboundContact

router = APIRouter(prefix="/outbound-contacts", tags=["outbound"])


@router.get("")
def list_outbound_contacts(db: Session = Depends(get_db)):
    return db.query(OutboundContact).all()
