from marshmallow import validates_schema, fields, ValidationError, validate

from app import ma
from app.domain.User import User


class UserResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ['password']


class BaseUserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True, validate=[validate.Email()])
    birth_date = fields.Str(required=True)
    about_me = fields.Str(allow_none=True)

    @validates_schema
    def validate_email(self, data, **kwargs):
        email = data.get('email')
        id = data.get('id')
        user = User.query.filter(User.email == email).first()
        if user and user.id != id:
            raise ValidationError('Email already exists.')

    @validates_schema
    def validate_username(self, data, **kwargs):
        username = data.get('username')
        id = data.get('id')
        user = User.query.filter(User.username == username).first()
        if user and user.id != id:
            raise ValidationError('Username already exists.')


class UserCreateSchema(BaseUserSchema):
    password = fields.Str(required=True, load_only=True)


class UserUpdateSchema(BaseUserSchema):
    id = fields.Integer(required=True)
