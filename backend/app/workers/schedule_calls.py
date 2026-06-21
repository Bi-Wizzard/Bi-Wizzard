from datetime import datetime

from app.services.compliance_engine import CalendarService, ComplianceEngine
from app.services.dialer_scheduler import DialerScheduler


def run_schedule_calls() -> None:
    compliance = ComplianceEngine()
    calendar = CalendarService()
    scheduler = DialerScheduler()

    now = datetime.utcnow()
    # Placeholder data for demo.
    result = compliance.check_contact_allowed(
        channel="VOICE",
        consent=True,
        is_opt_out=False,
        within_calendar=calendar.is_within_calendar(now),
        attempts_today=0,
        attempts_week=0,
        max_daily=3,
        max_weekly=10,
    )
    if result.allowed:
        scheduler.schedule_contact(now)
