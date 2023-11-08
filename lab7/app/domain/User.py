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
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    birth_date: Mapped[str] = mapped_column(String(30), nullable=True)
    image_file_name: Mapped[str] = mapped_column(String(200), nullable=True)

    @property
    def password(self):
        raise AttributeError('You cannot read password')

    @password.setter
    def password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class UserDetails:
    def __init__(self, login, first_name, last_name, email, birth_date, image_file_name):
        self.login = login
        self.first_name = login
        self.last_name = login
        self.email = login
        self.birth_date = login
        self.image_file_name = login

    @staticmethod
    def createUserDetails(user: User):
        user_details = UserDetails(user.username, user.first_name, user.last_name, user.email, user.birth_date,
                                   user.image_file_name)
        return user_details
