from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.import_job import ImportJob

router = APIRouter(prefix="/imports", tags=["imports"])


@router.post("/debtors")
def import_debtors(
    file: UploadFile = File(...),
    idempotency_key: str = Form(...),
    db: Session = Depends(get_db),
):
    job = ImportJob(tenant_id="TODO", file_name=file.filename, status="PENDING")
    db.add(job)
    db.commit()
    return {"job_id": job.id, "status": job.status, "idempotency_key": idempotency_key}
