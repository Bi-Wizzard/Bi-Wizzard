from datetime import datetime, time

from sqlalchemy import Date, DateTime, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class Calendar(Base):
    __tablename__ = "calendars"

    id: Mapped[str] = mapped_column(primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    timezone: Mapped[str] = mapped_column(String, default="America/Santiago", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class CalendarAllowedDay(Base):
    __tablename__ = "calendar_allowed_days"

    id: Mapped[str] = mapped_column(primary_key=True)
    calendar_id: Mapped[str] = mapped_column(ForeignKey("calendars.id"), nullable=False)
    day_of_week: Mapped[int] = mapped_column(nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)


class CalendarHoliday(Base):
    __tablename__ = "calendar_holidays"

    id: Mapped[str] = mapped_column(primary_key=True)
    calendar_id: Mapped[str] = mapped_column(ForeignKey("calendars.id"), nullable=False)
    holiday_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    description: Mapped[str | None] = mapped_column(String)
