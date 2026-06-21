-- Schema for Collections Autodialer (PostgreSQL)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Enums
DO $$ BEGIN
  CREATE TYPE campaign_type AS ENUM ('VOICE', 'EMAIL', 'MIXED');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN
  CREATE TYPE campaign_status AS ENUM ('DRAFT', 'ACTIVE', 'PAUSED', 'COMPLETED');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN
  CREATE TYPE channel_type AS ENUM ('VOICE', 'EMAIL');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN
  CREATE TYPE outbound_status AS ENUM ('PENDING', 'SCHEDULED', 'IN_PROGRESS', 'DONE', 'FAILED', 'BLOCKED');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN
  CREATE TYPE attempt_outcome AS ENUM ('ANSWERED', 'NO_ANSWER', 'BUSY', 'FAILED', 'VOICEMAIL');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN
  CREATE TYPE email_status AS ENUM ('QUEUED', 'SENT', 'DELIVERED', 'BOUNCED', 'FAILED');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN
  CREATE TYPE import_status AS ENUM ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Tenants
CREATE TABLE IF NOT EXISTS tenants (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  deleted_at timestamptz
);

-- RBAC
CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  email text NOT NULL,
  full_name text,
  is_active boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  deleted_at timestamptz,
  UNIQUE (tenant_id, email)
);

CREATE TABLE IF NOT EXISTS roles (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  name text NOT NULL,
  description text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, name)
);

CREATE TABLE IF NOT EXISTS permissions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL UNIQUE,
  description text
);

CREATE TABLE IF NOT EXISTS user_roles (
  user_id uuid NOT NULL REFERENCES users(id),
  role_id uuid NOT NULL REFERENCES roles(id),
  PRIMARY KEY (user_id, role_id)
);

CREATE TABLE IF NOT EXISTS role_permissions (
  role_id uuid NOT NULL REFERENCES roles(id),
  permission_id uuid NOT NULL REFERENCES permissions(id),
  PRIMARY KEY (role_id, permission_id)
);

-- Debtors
CREATE TABLE IF NOT EXISTS debtors (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  external_ref text,
  rut text,
  full_name text NOT NULL,
  tramo_mora text,
  consent_voice boolean NOT NULL DEFAULT true,
  consent_email boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  deleted_at timestamptz,
  UNIQUE (tenant_id, external_ref)
);

CREATE TABLE IF NOT EXISTS debtor_phones (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  debtor_id uuid NOT NULL REFERENCES debtors(id),
  phone_number text NOT NULL,
  priority smallint NOT NULL CHECK (priority BETWEEN 1 AND 3),
  is_primary boolean NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (debtor_id, phone_number)
);

CREATE TABLE IF NOT EXISTS debtor_emails (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  debtor_id uuid NOT NULL REFERENCES debtors(id),
  email text NOT NULL,
  is_primary boolean NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (debtor_id, email)
);

CREATE TABLE IF NOT EXISTS debtor_opt_outs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  debtor_id uuid NOT NULL REFERENCES debtors(id),
  channel channel_type,
  reason text,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (debtor_id, channel)
);

-- Debts
CREATE TABLE IF NOT EXISTS debts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  debtor_id uuid NOT NULL REFERENCES debtors(id),
  amount numeric(14,2) NOT NULL,
  currency text NOT NULL DEFAULT 'CLP',
  due_date date,
  status text NOT NULL DEFAULT 'OPEN',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

-- Campaigns + Segments
CREATE TABLE IF NOT EXISTS campaigns (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  name text NOT NULL,
  type campaign_type NOT NULL,
  status campaign_status NOT NULL DEFAULT 'DRAFT',
  dialing_strategy jsonb NOT NULL DEFAULT '{}',
  schedule_calendar_id uuid,
  created_by uuid REFERENCES users(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  deleted_at timestamptz
);

CREATE TABLE IF NOT EXISTS segments (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  name text NOT NULL,
  sql_filter text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, name)
);

CREATE TABLE IF NOT EXISTS campaign_segments (
  campaign_id uuid NOT NULL REFERENCES campaigns(id),
  segment_id uuid NOT NULL REFERENCES segments(id),
  PRIMARY KEY (campaign_id, segment_id)
);

-- Compliance rules & calendars
CREATE TABLE IF NOT EXISTS compliance_rules (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  name text NOT NULL,
  rule_type text NOT NULL,
  parameters jsonb NOT NULL DEFAULT '{}',
  is_active boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS campaign_compliance_rules (
  campaign_id uuid NOT NULL REFERENCES campaigns(id),
  compliance_rule_id uuid NOT NULL REFERENCES compliance_rules(id),
  priority smallint NOT NULL DEFAULT 100,
  PRIMARY KEY (campaign_id, compliance_rule_id)
);

CREATE TABLE IF NOT EXISTS calendars (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  name text NOT NULL,
  timezone text NOT NULL DEFAULT 'America/Santiago',
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS calendar_allowed_days (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  calendar_id uuid NOT NULL REFERENCES calendars(id),
  day_of_week smallint NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
  start_time time NOT NULL,
  end_time time NOT NULL,
  UNIQUE (calendar_id, day_of_week, start_time, end_time)
);

CREATE TABLE IF NOT EXISTS calendar_holidays (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  calendar_id uuid NOT NULL REFERENCES calendars(id),
  holiday_date date NOT NULL,
  description text,
  UNIQUE (calendar_id, holiday_date)
);

-- Outbound contacts (queue)
CREATE TABLE IF NOT EXISTS outbound_contacts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  campaign_id uuid NOT NULL REFERENCES campaigns(id),
  debtor_id uuid NOT NULL REFERENCES debtors(id),
  channel channel_type NOT NULL,
  scheduled_for timestamptz NOT NULL,
  status outbound_status NOT NULL DEFAULT 'PENDING',
  attempts_count int NOT NULL DEFAULT 0,
  correlation_id uuid,
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Call attempts
CREATE TABLE IF NOT EXISTS call_attempts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  campaign_id uuid NOT NULL REFERENCES campaigns(id),
  debtor_id uuid NOT NULL REFERENCES debtors(id),
  debtor_phone_id uuid NOT NULL REFERENCES debtor_phones(id),
  attempt_at timestamptz NOT NULL DEFAULT now(),
  status text NOT NULL DEFAULT 'COMPLETED',
  outcome attempt_outcome,
  provider_message_id text,
  correlation_id uuid,
  created_by uuid REFERENCES users(id),
  idempotency_key text,
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Email templates and sends
CREATE TABLE IF NOT EXISTS email_templates (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  name text NOT NULL,
  subject text NOT NULL,
  body text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS email_sends (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  campaign_id uuid NOT NULL REFERENCES campaigns(id),
  debtor_id uuid NOT NULL REFERENCES debtors(id),
  debtor_email_id uuid NOT NULL REFERENCES debtor_emails(id),
  template_id uuid NOT NULL REFERENCES email_templates(id),
  status email_status NOT NULL DEFAULT 'QUEUED',
  provider_message_id text,
  sent_at timestamptz,
  correlation_id uuid,
  created_by uuid REFERENCES users(id),
  idempotency_key text,
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Import jobs
CREATE TABLE IF NOT EXISTS import_jobs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  file_name text NOT NULL,
  status import_status NOT NULL DEFAULT 'PENDING',
  created_by uuid REFERENCES users(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS import_job_errors (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  import_job_id uuid NOT NULL REFERENCES import_jobs(id),
  row_number int NOT NULL,
  error_message text NOT NULL,
  raw_data jsonb NOT NULL DEFAULT '{}'
);

-- Audit log (append-only)
CREATE TABLE IF NOT EXISTS audit_log (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  actor_user_id uuid REFERENCES users(id),
  action text NOT NULL,
  entity_type text NOT NULL,
  entity_id uuid,
  payload jsonb NOT NULL DEFAULT '{}',
  correlation_id uuid,
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Idempotency
CREATE TABLE IF NOT EXISTS idempotency_keys (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  key text NOT NULL,
  endpoint text NOT NULL,
  request_hash text NOT NULL,
  response_code int,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, key, endpoint)
);

-- Reporting-friendly indexes
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns (tenant_id, status);
CREATE INDEX IF NOT EXISTS idx_debtors_lookup ON debtors (tenant_id, rut, full_name);
CREATE INDEX IF NOT EXISTS idx_call_attempts_by_date ON call_attempts (tenant_id, attempt_at);
CREATE INDEX IF NOT EXISTS idx_email_sends_by_date ON email_sends (tenant_id, sent_at);
CREATE INDEX IF NOT EXISTS idx_outbound_contacts_status ON outbound_contacts (tenant_id, status, scheduled_for);

-- Seed roles/permissions and compliance rule examples
INSERT INTO permissions (id, name, description) VALUES
  (gen_random_uuid(), 'campaign.read', 'Read campaigns'),
  (gen_random_uuid(), 'campaign.write', 'Create/update campaigns'),
  (gen_random_uuid(), 'debtor.read', 'Read debtors'),
  (gen_random_uuid(), 'debtor.write', 'Create/update debtors'),
  (gen_random_uuid(), 'dialer.execute', 'Run dialer actions')
ON CONFLICT (name) DO NOTHING;

-- Example compliance rules (Ley de Cobranza)
INSERT INTO compliance_rules (id, tenant_id, name, rule_type, parameters)
VALUES
  (gen_random_uuid(), gen_random_uuid(), 'Horario habil', 'CALENDAR_WINDOW', '{"start":"09:00","end":"20:00"}'),
  (gen_random_uuid(), gen_random_uuid(), 'Max intentos diarios', 'MAX_ATTEMPTS_PER_DAY', '{"max":3}')
ON CONFLICT DO NOTHING;
