from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app import data_base


class User(data_base.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(20), nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    birth_date: Mapped[str] = mapped_column(String(30), nullable=True)
    image_file_name: Mapped[str] = mapped_column(String(200), nullable=True)

    @property
    def user_password(self):
        raise AttributeError('You cannot read password')

    @user_password.setter
    def user_password(self, new_password):
        self.password = generate_password_hash(new_password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def create_user_details(self):
        return {
            'login': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'email': self.email,
            'phone_number': '+1000000000'
        }
