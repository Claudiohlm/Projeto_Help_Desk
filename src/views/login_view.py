from flask_restful import Resource
from flask import request, jsonify, make_response
from src.services import usuario_service
from src import api


class Login(Resource):
    """
    Autenticacao. Verifica a senha criptografada (argon2) e
    retorna tambem o TIPO do usuario (admin/comum), que o front
    usa para liberar ou bloquear acoes.
    """
    def post(self):
        dados = request.json

        if not dados or not dados.get('email') or not dados.get('senha'):
            return make_response(jsonify({'message': 'Email e senha sao obrigatorios.'}), 400)

        usuario = usuario_service.listar_usuario_email(dados['email'])

        if not usuario:
            return make_response(jsonify({'message': 'Usuario nao encontrado.'}), 404)

        if usuario.verifica_senha(dados['senha']):
            return make_response(jsonify({
                'message': 'Login realizado com sucesso!',
                'usuario': {
                    'id': usuario.id,
                    'nome': usuario.nome,
                    'email': usuario.email,
                    'tipo': usuario.tipo      # admin ou comum
                }
            }), 200)
        else:
            return make_response(jsonify({'message': 'Senha incorreta.'}), 401)


api.add_resource(Login, '/login')
