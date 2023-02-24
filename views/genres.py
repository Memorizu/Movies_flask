from flask import request
from flask_restx import Resource, Namespace
from utils import admin_required, auth_required
from dao.model.genre import GenreSchema
from implemented import genre_service


genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):

    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        genre_service.create(req_json)
        return '', 201


@genre_ns.route('/<int:genre_id>')
class GenreView(Resource):

    @auth_required
    def get(self, genre_id):
        r = genre_service.get_one(genre_id)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, genre_id):
        req_json = request.json
        genre_service.update(genre_id, req_json)
        return '', 204

    @admin_required
    def delete(self, genre_id):
        genre_service.delete(genre_id)
        return '', 204
