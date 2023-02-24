from flask import request
from flask_restx import Namespace, Resource

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UserViews(Resource):

    def get(self):
        users = user_service.get_all()
        return UserSchema(many=True).dump(users)

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return UserSchema().dumps(user)


@user_ns.route('/<int:uid>')
class UserViews(Resource):

    def get(self, uid):
        user = user_service.get_one(uid)
        return UserSchema().dump(user)

    def put(self, uid):
        return ''

    def delete(self, uid):
        user_service.delete(uid)
        return '', 204
