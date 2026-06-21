from dataclasses import dataclass
from datetime import datetime


@dataclass
class ComplianceResult:
    allowed: bool
    reason_code: str | None = None


class ComplianceEngine:
    """Evaluates configurable compliance rules (Ley de Cobranza).

    Defaults are conservative and deny if data is missing.
    """

    def check_contact_allowed(
        self,
        *,
        channel: str,
        consent: bool,
        is_opt_out: bool,
        within_calendar: bool,
        attempts_today: int,
        attempts_week: int,
        max_daily: int,
        max_weekly: int,
    ) -> ComplianceResult:
        if not consent:
            return ComplianceResult(False, "NO_CONSENT")
        if is_opt_out:
            return ComplianceResult(False, "DO_NOT_CONTACT")
        if not within_calendar:
            return ComplianceResult(False, "OUTSIDE_CALENDAR")
        if attempts_today >= max_daily:
            return ComplianceResult(False, "MAX_DAILY")
        if attempts_week >= max_weekly:
            return ComplianceResult(False, "MAX_WEEKLY")
        return ComplianceResult(True)


class CalendarService:
    def is_within_calendar(self, now: datetime) -> bool:
        # Placeholder: implement table-driven calendar lookup.
        return True
