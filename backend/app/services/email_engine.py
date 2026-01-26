from dataclasses import dataclass


@dataclass
class EmailSendResult:
    queued: bool
    provider_message_id: str | None = None


class EmailEngine:
    """Abstract email provider integration."""

    def send_email(self, to_address: str, subject: str, body: str) -> EmailSendResult:
        # Placeholder: integrate SMTP/HTTP provider here.
        return EmailSendResult(queued=True, provider_message_id="mock-id")
