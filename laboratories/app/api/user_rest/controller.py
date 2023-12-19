from flask import request
from flask_restful import Resource

from app import data_base
from app.domain.User import User
from app.api.user_rest.schemas import UserResponseSchema, UserCreateSchema, UserUpdateSchema


class UserRestController(Resource):

    def get(self, id: int):
        user = User.query.get(id)
        if not user:
            return {'error': 'User is not found.'}, 404
        return UserResponseSchema().dump(user), 200

    def post(self):
        schema = UserCreateSchema()
        user = schema.load(request.json)

        user.user_password = user.password
        data_base.session.add(user)
        data_base.session.commit()

        return UserResponseSchema().dump(user), 201

    def put(self):
        updated_user_dto = UserUpdateSchema()
        updated_user = updated_user_dto.load(request.json)

        existent: User = User.query.get(updated_user.id)
        if not existent:
            return {'error': 'User is not found.'}, 404

        existent.first_name = updated_user.first_name
        existent.last_name = updated_user.last_name
        existent.email = updated_user.email
        existent.username = updated_user.username
        existent.birth_date = updated_user.birth_date
        existent.about_me = updated_user.about_me

        data_base.session.commit()
        return UserResponseSchema().dump(existent), 200

    def delete(self, id):
        existent: User = User.query.get(id)
        if not existent:
            return {'error': 'User is not found.'}, 404

        data_base.session.delete(existent)
        data_base.session.commit()
        return {}, 204


class UserListRestController(Resource):

    def get(self):
        users = User.query.all()
        schema = UserResponseSchema(many=True)
        return schema.dump(users), 200
