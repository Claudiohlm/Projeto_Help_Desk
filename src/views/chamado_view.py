from flask_restful import Resource
from marshmallow import ValidationError
from src.schemas import chamado_schema
from flask import request, jsonify, make_response
from src.services import chamado_service
from src import api


# helper: le quem e o usuario a partir dos parametros da requisicao
# (id e tipo vem do front, que guarda isso apos o login)
def get_contexto():
    usuario_id = request.args.get("usuario_id", type=int)
    tipo = request.args.get("tipo", default="comum")
    return usuario_id, tipo


# ============================================================
# /chamados
# ============================================================
class ChamadoList(Resource):
    def get(self):
        usuario_id, tipo = get_contexto()
        status = request.args.get("status")

        if not usuario_id:
            return make_response(jsonify({"message": "Usuario nao identificado."}), 400)

        chamados = chamado_service.listar_chamado(usuario_id, tipo, status)

        if not chamados:
            return make_response(jsonify([]), 200)

        schema = chamado_schema.ChamadoSchema(many=True)
        return make_response(jsonify(schema.dump(chamados)), 200)

    def post(self):
        schema = chamado_schema.ChamadoSchema()
        try:
            dados = schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

        try:
            # prioridade NAO vem do usuario — o service define pela categoria
            resultado = chamado_service.cadastrar_chamado(dados)
            return make_response(jsonify(schema.dump(resultado)), 201)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 400)


api.add_resource(ChamadoList, '/chamados')


# ============================================================
# /chamados/<id>
# ============================================================
class ChamadoResource(Resource):
    def get(self, id_chamado):
        usuario_id, tipo = get_contexto()
        chamado = chamado_service.listar_chamado_id(id_chamado)

        if not chamado:
            return make_response(jsonify({'message': "Chamado nao encontrado."}), 404)

        # regra: usuario comum so acessa o proprio chamado
        if not chamado_service.pode_acessar(chamado, usuario_id, tipo):
            return make_response(jsonify({'message': "Voce nao tem permissao para ver este chamado."}), 403)

        schema = chamado_schema.ChamadoSchema()
        return make_response(jsonify(schema.dump(chamado)), 200)

    def put(self, id_chamado):
        # usado para mudar status — REGRA: somente admin
        usuario_id, tipo = get_contexto()
        dados = request.json or {}
        novo_status = dados.get('status')

        if not novo_status:
            return make_response(jsonify({'message': 'Informe o status.'}), 400)

        chamado, erro = chamado_service.mudar_status(id_chamado, novo_status, tipo)

        if erro == "sem_permissao":
            return make_response(jsonify({'message': 'Apenas administradores podem mudar o status.'}), 403)
        if erro == "nao_encontrado":
            return make_response(jsonify({'message': 'Chamado nao encontrado.'}), 404)
        if erro == "fechado":
            return make_response(jsonify({'message': 'Chamado fechado nao pode ser alterado.'}), 422)

        schema = chamado_schema.ChamadoSchema()
        return make_response(jsonify(schema.dump(chamado)), 200)

    def delete(self, id_chamado):
        if chamado_service.deletar_chamado(id_chamado):
            return make_response(jsonify({'message': 'Chamado deletado com sucesso!'}), 200)
        return make_response(jsonify({'message': 'Chamado nao encontrado!'}), 400)


api.add_resource(ChamadoResource, '/chamados/<int:id_chamado>')


# ============================================================
# /chamados/<id>/respostas
# ============================================================
class RespostaList(Resource):
    def get(self, id_chamado):
        respostas = chamado_service.listar_respostas(id_chamado)
        schema = chamado_schema.RespostaSchema(many=True)
        return make_response(jsonify(schema.dump(respostas)), 200)

    def post(self, id_chamado):
        schema = chamado_schema.RespostaSchema()
        try:
            dados = schema.load(request.json)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

        resposta, erro = chamado_service.cadastrar_resposta(id_chamado, dados)

        if erro == "nao_encontrado":
            return make_response(jsonify({'message': 'Chamado nao encontrado.'}), 404)
        if erro == "fechado":
            return make_response(jsonify({'message': 'Nao e possivel responder um chamado fechado.'}), 422)

        return make_response(jsonify(schema.dump(resposta)), 201)


api.add_resource(RespostaList, '/chamados/<int:id_chamado>/respostas')


# ============================================================
# /respostas/<id>
# ============================================================
class RespostaResource(Resource):
    def delete(self, id_resposta):
        if chamado_service.deletar_resposta(id_resposta):
            return make_response(jsonify({'message': 'Resposta deletada com sucesso!'}), 200)
        return make_response(jsonify({'message': 'Resposta nao encontrada!'}), 400)


api.add_resource(RespostaResource, '/respostas/<int:id_resposta>')
