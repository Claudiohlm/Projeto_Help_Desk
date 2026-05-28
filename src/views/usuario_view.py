from flask_restful import Resource
from marshmallow import ValidationError
from src.schemas import usuario_schema
from flask import request, jsonify, make_response
from src.models.usuario_model import UsuarioModel
from src.services import usuario_service
from src import api


class UsuarioList(Resource):
    def get(self):
        # faz a query
        usuarios = usuario_service.listar_usuario()

        # verifica se tem usuario
        if not usuarios:
            return make_response(jsonify({"message":"Não existe usuarios!"}), 404)
        
        schema = usuario_schema.UsuarioSchema(many=True)
        # retorna com os usuarios
        return make_response(jsonify(schema.dump(usuarios)), 200)
        
    def post(self):
        schema = usuario_schema.UsuarioSchema()

        try:
            dados = schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)
        
        if usuario_service.listar_usuario_email(dados['email']):
            return make_response(jsonify({'message':'E-mail já cadastrado.'}), 400)

        try:
            novo_usuario = UsuarioModel(
                nome =dados['nome'],
                email=dados['email'],
                senha=dados['senha']
            )
            resultado = usuario_service.cadastrar_usuario(novo_usuario)
            return make_response(jsonify(schema.dump(resultado)), 201)
        
        except Exception as e:
            return make_response(jsonify({'message':str(e)}), 400)

api.add_resource(UsuarioList, '/usuarios')


class UsuarioResource(Resource):
    def get(self, id_usuario):
        usuario = usuario_service.listar_usuario_id(id_usuario)
        if usuario:
            schema = usuario_schema.UsuarioSchema()
            return make_response(jsonify(schema.dump(usuario)), 200)
        return make_response(jsonify({'message':"Usuario não encontrado."}), 404)
    


    def put(self, id_usuario):
        schema = usuario_schema.UsuarioSchema()
        try:
            dados = schema.load(request.json)
        
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)
        
        usuario = usuario_service.editar_usuario(id_usuario, dados)

        if usuario:
            return make_response(jsonify(schema.dump(usuario)), 200)
        return make_response(jsonify({'message':'Usuario não encontrado.'}), 404)

    def delete(self, id_usuario):
        if usuario_service.deletar_usuario(id_usuario):
            return make_response(jsonify({'message':'Usuário deletado com sucesso!'}), 200)
        return make_response(jsonify({'message':'Usuário não encontrado!'}), 400)


api.add_resource(UsuarioResource, '/usuarios/<int:id_usuario>')