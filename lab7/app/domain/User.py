from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app import data_base


class User(data_base.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    birth_date: Mapped[str] = mapped_column(String(30), nullable=True)
    image_file_name: Mapped[str] = mapped_column(String(200), nullable=True)
