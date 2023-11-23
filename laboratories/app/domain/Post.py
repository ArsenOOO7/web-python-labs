from enum import Enum

from sqlalchemy import Integer, String, Enum as Enumeration, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app import data_base

post_tags = data_base.Table(
    'post_tags',
    data_base.Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    data_base.Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class PostType(Enum):
    NEWS = "NEWS"
    PUBLICATION = "PUBLICATION"
    OTHER = "OTHER"


class Post(data_base.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    image: Mapped[str] = mapped_column(String(255), server_default='post_default.png')
    enabled: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    type: Mapped[str] = mapped_column(Enumeration(PostType), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'), nullable=False)
    tags = relationship('Tag', secondary=post_tags, backref='posts')
