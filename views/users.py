from flask_restx import Namespace, Resource

user_ns = Namespace('users')


@user_ns.route('/')
class UserViews(Resource):

    def get(self):
        return ''

    def post(self):
        return ''


@user_ns.route('/<int:uid>')
class UserViews(Resource):

    def get(self, uid):
        return ''

    def put(self, uid):
        return ''

    def delete(self, uid):
        return ''
