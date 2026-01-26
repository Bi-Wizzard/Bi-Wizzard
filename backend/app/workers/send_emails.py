from datetime import datetime

from app.services.compliance_engine import CalendarService, ComplianceEngine
from app.services.email_engine import EmailEngine


def run_send_emails() -> None:
    compliance = ComplianceEngine()
    calendar = CalendarService()
    email_engine = EmailEngine()

    now = datetime.utcnow()
    result = compliance.check_contact_allowed(
        channel="EMAIL",
        consent=True,
        is_opt_out=False,
        within_calendar=calendar.is_within_calendar(now),
        attempts_today=0,
        attempts_week=0,
        max_daily=2,
        max_weekly=5,
    )
    if result.allowed:
        email_engine.send_email(
            to_address="cliente@example.com",
            subject="Aviso de cobranza",
            body="Estimado cliente...",
        )
