from flask_restful import Resource
from marshmallow import ValidationError
from src.schemas import usuario_schema
from flask import request, jsonify, make_response
from src.models.usuario_model import UsuarioModel
from src.services import usuario_service
from src import api


class UsuarioList(Resource):
    def get(self):
        usuarios = usuario_service.listar_usuario()
        if not usuarios:
            return make_response(jsonify({"message": "Nao existe usuarios!"}), 404)
        schema = usuario_schema.UsuarioSchema(many=True)
        return make_response(jsonify(schema.dump(usuarios)), 200)

    def post(self):
        dados = request.json or {}

        if not dados.get('nome') or not dados.get('email') or not dados.get('senha'):
            return make_response(jsonify({'message': 'Nome, email e senha sao obrigatorios.'}), 400)

        if usuario_service.listar_usuario_email(dados['email']):
            return make_response(jsonify({'message': 'E-mail ja cadastrado.'}), 400)

        try:
            # cadastro pelo site cria SEMPRE usuario comum.
            # o admin e criado de fabrica pelo script criar_admin.py
            novo_usuario = UsuarioModel(
                nome=dados['nome'],
                email=dados['email'],
                senha="",
                tipo="comum"
            )
            novo_usuario.gen_senha(dados['senha'])
            resultado = usuario_service.cadastrar_usuario_obj(novo_usuario)

            return make_response(jsonify({
                'id': resultado.id,
                'nome': resultado.nome,
                'email': resultado.email,
                'tipo': resultado.tipo
            }), 201)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 400)


api.add_resource(UsuarioList, '/usuarios')


class UsuarioResource(Resource):
    def get(self, id_usuario):
        usuario = usuario_service.listar_usuario_id(id_usuario)
        if usuario:
            schema = usuario_schema.UsuarioSchema()
            return make_response(jsonify(schema.dump(usuario)), 200)
        return make_response(jsonify({'message': "Usuario nao encontrado."}), 404)

    def delete(self, id_usuario):
        if usuario_service.deletar_usuario(id_usuario):
            return make_response(jsonify({'message': 'Usuario deletado com sucesso!'}), 200)
        return make_response(jsonify({'message': 'Usuario nao encontrado!'}), 400)


api.add_resource(UsuarioResource, '/usuarios/<int:id_usuario>')
