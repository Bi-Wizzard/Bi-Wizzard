# Arquitectura (Plataforma de Cobranza Autodialer)

## Servicios / Módulos
- **API Gateway (FastAPI)**
  - Autenticación, idempotencia, validación, RBAC.
  - Encola acciones con `correlation_id`.
- **Compliance Engine**
  - Evalúa reglas configurables (Ley de Cobranza) por canal.
  - Valida calendario/feriados y límites de contacto.
- **Dialer Scheduler**
  - Selecciona deudores por segmentos y estrategia.
  - Genera `outbound_contacts` (VOICE/EMAIL).
- **Email Engine**
  - Envíos por proveedor abstracto (SMTP/HTTP).
  - Tracking de estados y `provider_message_id`.
- **Audit/Event Log**
  - Bitácora append-only con `correlation_id`.
  - Outbox de eventos para integraciones futuras.
- **Workers**
  - `schedule_calls`: planifica llamadas.
  - `send_emails`: ejecuta envíos permitidos.

## Datos clave
- Multi-tenant: `tenant_id` en tablas operativas.
- RBAC: usuarios/roles/permisos con tablas join.
- Deudores: 3 teléfonos max, emails, opt-out.
- Campañas: VOICE/EMAIL/MIXED con reglas y calendario.
- Cumplimiento: reglas parametrizadas en JSONB.
- Auditoría: todas las acciones con `actor_user_id`.

## Flujos principales (resumen)
- **Importación CSV** → valida filas → crea deudores/deudas.
- **Planificación** → aplica cumplimiento → genera cola.
- **Ejecución** → realiza intentos → registra outcomes.
- **Escalamiento** → si fallan llamadas, encola email.
