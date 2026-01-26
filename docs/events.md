# Eventos (nombres + payloads)

## campaign.scheduled
```json
{
  "event_id": "uuid",
  "event_type": "campaign.scheduled",
  "tenant_id": "uuid",
  "campaign_id": "uuid",
  "scheduled_count": 120,
  "correlation_id": "uuid",
  "occurred_at": "2024-01-01T10:00:00Z"
}
```

## call.attempted
```json
{
  "event_id": "uuid",
  "event_type": "call.attempted",
  "tenant_id": "uuid",
  "campaign_id": "uuid",
  "debtor_id": "uuid",
  "debtor_phone_id": "uuid",
  "status": "COMPLETED",
  "outcome": "NO_ANSWER",
  "attempted_at": "2024-01-01T10:05:00Z",
  "correlation_id": "uuid"
}
```

## email.sent
```json
{
  "event_id": "uuid",
  "event_type": "email.sent",
  "tenant_id": "uuid",
  "campaign_id": "uuid",
  "debtor_id": "uuid",
  "template_id": "uuid",
  "delivery_status": "SENT",
  "provider_message_id": "abc-123",
  "correlation_id": "uuid"
}
```

## compliance.blocked
```json
{
  "event_id": "uuid",
  "event_type": "compliance.blocked",
  "tenant_id": "uuid",
  "campaign_id": "uuid",
  "debtor_id": "uuid",
  "channel": "EMAIL",
  "reason_code": "DO_NOT_CONTACT",
  "correlation_id": "uuid"
}
```
