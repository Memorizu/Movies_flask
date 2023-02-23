from flask import request
from flask_restx import Namespace, Resource

from dao.model.user import user_schema
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UserViews(Resource):

    def get(self):
        users = user_service.get_all()
        return user_schema(many=True).dumps(users)

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return user_schema.dumps(user)


@user_ns.route('/<int:uid>')
class UserViews(Resource):

    def get(self, uid):
        return ''

    def put(self, uid):
        return ''

    def delete(self, uid):
        return ''
