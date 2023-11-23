from enum import Enum

from sqlalchemy import Integer, String, Enum as Enumeration
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import data_base


class Color(Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    SUCCESS = "SUCCESS"
    DANGER = "DANGER"
    WARNING = "WARNING"
    INFO = "INFO"
    LIGHT = "LIGHT"
    DARK = "DARK"


class Tag(data_base.Model):
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    color: Mapped[str] = mapped_column(Enumeration(Color), nullable=False, default=Color.PRIMARY)
