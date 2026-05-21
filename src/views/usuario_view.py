from flask_restful import Resource
from marshmallow import ValidationError
from src.schemas import usuario_schema
from flask import request, jsonify, make_response
from src.models.usuario_model import UsuarioModel
from src.services import usuario_service
from src import api


class UsuarioList(Resource):
    def get(self):
        ...
    
    def post(self):
        ...

api.add_resource(UsuarioList, '/usuarios')


class UsuarioResource(Resource):
    def get(self, id_usuario):
        ...

    def put(self, id_usuario):
        ...

    def delete(self, id_usuario):
        ...


api.add_resource(UsuarioResource, '/usuarios/<int:id_usuario>')