import datetime
from enum import Enum

from sqlalchemy import Integer, Enum as SQLEnum, String, Float, Date
from sqlalchemy.orm import Mapped, mapped_column

from app import data_base


class HouseholdApplianceType(Enum):
    KITCHEN = 'KITCHEN'
    LAUNDRY = 'LAUNDRY'
    CLEANING = 'CLEANING'
    ENTERTAINMENT = 'ENTERTAINMENT'
    HOME_OFFICE = 'HOME_OFFICE'


class HouseholdAppliance(data_base.Model):
    __tablename__ = 'household_appliances'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(SQLEnum(HouseholdApplianceType), nullable=False)
    name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True, index=True)
    brand: Mapped[str] = mapped_column(String(40), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    purchased_at: Mapped[datetime.date] = mapped_column(Date, nullable=True)
