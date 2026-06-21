# Flujos (pasos secuenciales)

## 1) Importación de deudores y deudas (CSV)
1. `POST /imports/debtors` con archivo CSV + idempotency_key.
2. API crea `import_jobs` y `import_job_errors`.
3. Worker valida y persiste `debtors`, `debts`, contactos.
4. Se registra `audit_log` con `correlation_id`.

## 2) Programación de llamadas (VOICE)
1. `POST /campaigns/{id}/schedule`.
2. API consulta segmentos asociados y construye población.
3. Compliance Engine verifica:
   - Calendario permitido + feriados.
   - Límite de intentos por día/semana.
   - Do-not-contact + opt-out.
4. Dialer Scheduler crea `outbound_contacts` (VOICE).
5. Worker `schedule_calls` consume cola.

## 3) Envío de email (EMAIL)
1. API/Worker solicita envío para deudor.
2. Compliance Engine valida:
   - Consentimiento email.
   - Límite por canal.
   - Calendario permitido.
3. Email Engine genera `email_sends` y entrega a proveedor.
4. Se actualiza `delivery_status` y `provider_message_id`.

## 4) Escalamiento MIXED
1. Si llamadas fallan según estrategia → encola email.
2. Compliance Engine valida antes de crear `outbound_contacts`.
3. Worker envía email y registra outcomes.

## 5) Auditoría
1. Cada acción API/worker genera `audit_log`.
2. Todo registro incluye `correlation_id`.
