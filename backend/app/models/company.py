from datetime import datetime
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, Date

from app.db import Base


class TimeStampMixin:

    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Company(TimeStampMixin, Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    qliqs: Mapped[List["Qliq"]] = relationship(back_populates="company", cascade="all, delete")
    qoils: Mapped[List["Qoil"]] = relationship(back_populates="company", cascade="all, delete")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.email!r})"


class Qliq(TimeStampMixin, Base):
    __tablename__ = "qliqs"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"))
    company: Mapped["Company"] = relationship(back_populates="qliqs")

    data1_fact: Mapped[int | None]
    data2_fact: Mapped[int | None]
    data1_forecast: Mapped[int | None]
    data2_forecast: Mapped[int | None]

    metric_date = mapped_column(Date())


class Qoil(TimeStampMixin, Base):
    __tablename__ = "qoils"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"))
    company: Mapped["Company"] = relationship(back_populates="qoils")

    data1_fact: Mapped[int | None]
    data2_fact: Mapped[int | None]
    data1_forecast: Mapped[int | None]
    data2_forecast: Mapped[int | None]

    metric_date = mapped_column(Date())