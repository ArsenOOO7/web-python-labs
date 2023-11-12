from app import data_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Enum as Enumeration, DateTime
from sqlalchemy.sql import func

from enum import Enum


class Satisfaction(Enum):
    VERY_SATISFIED = 'VERY_SATISFIED'
    SATISFIED = 'SATISFIED'
    DISSATISFIED = 'DISSATISFIED'


class Feedback(data_base.Model):
    __tablename__ = "feedback"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    feedback: Mapped[str] = mapped_column(String, nullable=False)
    satisfaction: Mapped[str] = mapped_column(Enumeration(Satisfaction), nullable=False)
    user: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now(), nullable=False)
