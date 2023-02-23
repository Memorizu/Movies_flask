from flask import request, abort
from flask_restx import Namespace, Resource

from dao.model.user import User
from implemented import auth_service
from setup_db import db


auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthViews(Resource):

    def post(self):
        req_json = request.json
        return auth_service.create(req_json)


    def put(self):
        pass
