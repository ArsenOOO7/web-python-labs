from enum import Enum

from sqlalchemy import Integer, String, Enum as Enumeration, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app import data_base


class PostType(Enum):
    NEWS = "NEWS"
    PUBLICATION = "PUBLICATION"
    OTHER = "OTHER"


class Post(data_base.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    image: Mapped[str] = mapped_column(String(255), server_default='post_default.jpg')
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    type: Mapped[str] = mapped_column(Enumeration(PostType), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)