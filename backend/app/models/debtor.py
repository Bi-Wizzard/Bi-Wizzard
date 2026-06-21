from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class Debtor(Base):
    __tablename__ = "debtors"
    __table_args__ = (UniqueConstraint("tenant_id", "external_ref", name="uq_debtors_tenant_external"),)

    id: Mapped[str] = mapped_column(primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    external_ref: Mapped[str | None] = mapped_column(String)
    rut: Mapped[str | None] = mapped_column(String)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    tramo_mora: Mapped[str | None] = mapped_column(String)
    consent_voice: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    consent_email: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class DebtorPhone(Base):
    __tablename__ = "debtor_phones"
    __table_args__ = (UniqueConstraint("debtor_id", "phone_number", name="uq_debtor_phone"),)

    id: Mapped[str] = mapped_column(primary_key=True)
    debtor_id: Mapped[str] = mapped_column(ForeignKey("debtors.id"), nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    priority: Mapped[int] = mapped_column(nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class DebtorEmail(Base):
    __tablename__ = "debtor_emails"
    __table_args__ = (UniqueConstraint("debtor_id", "email", name="uq_debtor_email"),)

    id: Mapped[str] = mapped_column(primary_key=True)
    debtor_id: Mapped[str] = mapped_column(ForeignKey("debtors.id"), nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class DebtorOptOut(Base):
    __tablename__ = "debtor_opt_outs"
    __table_args__ = (UniqueConstraint("debtor_id", "channel", name="uq_debtor_optout"),)

    id: Mapped[str] = mapped_column(primary_key=True)
    debtor_id: Mapped[str] = mapped_column(ForeignKey("debtors.id"), nullable=False)
    channel: Mapped[str | None] = mapped_column(String)
    reason: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Debt(Base):
    __tablename__ = "debts"

    id: Mapped[str] = mapped_column(primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    debtor_id: Mapped[str] = mapped_column(ForeignKey("debtors.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String, default="CLP", nullable=False)
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String, default="OPEN", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
