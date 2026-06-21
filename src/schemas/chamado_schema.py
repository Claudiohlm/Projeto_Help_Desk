# criar os schemas para validacao e serializacao de chamado e resposta
from src import ma
from marshmallow import fields, validate


# ---------- RESPOSTA ----------
class RespostaSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    mensagem = fields.Str(required=True, validate=validate.Length(min=3))
    chamado_id = fields.Int(dump_only=True)
    usuario_id = fields.Int(required=True)
    criado_em = fields.DateTime(dump_only=True)


# ---------- CHAMADO ----------
class ChamadoSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(required=True, validate=validate.Length(min=3, max=200))
    descricao = fields.Str(required=True, validate=validate.Length(min=5))
    categoria = fields.Str(required=False, allow_none=True, validate=validate.Length(max=80))
    prioridade = fields.Str(
        required=False,
        load_default="media",
        validate=validate.OneOf(["baixa", "media", "alta", "critica"])
    )
    status = fields.Str(
        required=False,
        validate=validate.OneOf(["aberto", "em_atendimento", "resolvido", "fechado"])
    )
    usuario_id = fields.Int(required=True)
    criado_em = fields.DateTime(dump_only=True)
    atualizado_em = fields.DateTime(dump_only=True)

    # quando quiser retornar o chamado junto com as respostas
    respostas = fields.List(fields.Nested(RespostaSchema), dump_only=True)
