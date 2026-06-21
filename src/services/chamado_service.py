# camada de servico: regras de negocio e acesso ao banco para chamados e respostas
from ..models.chamado_model import ChamadoModel, RespostaModel
from src import db


# regra de negocio: prioridade definida automaticamente pela categoria
# software -> alta | hardware -> media | outras -> media (padrao)
def prioridade_por_categoria(categoria):
    if not categoria:
        return "media"
    cat = categoria.strip().lower()
    if cat == "software":
        return "alta"
    elif cat == "hardware":
        return "media"
    return "media"


# ---------------- CHAMADOS ----------------

# cadastrar chamado (a prioridade vem da categoria, nao do usuario)
def cadastrar_chamado(dados):
    prioridade = prioridade_por_categoria(dados.get('categoria'))
    chamado_db = ChamadoModel(
        titulo=dados['titulo'],
        descricao=dados['descricao'],
        categoria=dados.get('categoria'),
        prioridade=prioridade,        # definida automaticamente
        status="aberto",
        usuario_id=dados['usuario_id']
    )
    db.session.add(chamado_db)
    db.session.commit()
    return chamado_db


# listar chamados respeitando permissao:
# - admin ve todos
# - comum ve apenas os que ele criou
def listar_chamado(usuario_id, tipo, status=None):
    query = ChamadoModel.query

    # se nao for admin, filtra so os chamados do proprio usuario
    if tipo != "admin":
        query = query.filter_by(usuario_id=usuario_id)

    if status:
        query = query.filter_by(status=status)

    return query.order_by(ChamadoModel.criado_em.desc()).all()


# listar chamado por id
def listar_chamado_id(id):
    return ChamadoModel.query.get(id)


# verifica se o usuario pode acessar um chamado especifico
# (admin pode tudo; comum so o proprio)
def pode_acessar(chamado, usuario_id, tipo):
    if tipo == "admin":
        return True
    return chamado.usuario_id == usuario_id


# mudar status — REGRA: somente admin pode mudar status
def mudar_status(id, novo_status, tipo):
    # regra de negocio: so admin muda status
    if tipo != "admin":
        return None, "sem_permissao"

    chamado = ChamadoModel.query.get(id)
    if not chamado:
        return None, "nao_encontrado"

    if chamado.status == "fechado":
        return None, "fechado"

    chamado.status = novo_status
    db.session.commit()
    return chamado, None


# deletar chamado
def deletar_chamado(id):
    chamado = ChamadoModel.query.get(id)
    if chamado:
        db.session.delete(chamado)
        db.session.commit()
        return True
    return False


# ---------------- RESPOSTAS ----------------

def cadastrar_resposta(chamado_id, dados):
    chamado = ChamadoModel.query.get(chamado_id)
    if not chamado:
        return None, "nao_encontrado"

    if chamado.status == "fechado":
        return None, "fechado"

    if chamado.status == "aberto":
        chamado.status = "em_atendimento"

    resposta_db = RespostaModel(
        mensagem=dados['mensagem'],
        chamado_id=chamado_id,
        usuario_id=dados['usuario_id']
    )
    db.session.add(resposta_db)
    db.session.commit()
    return resposta_db, None


def listar_respostas(chamado_id):
    return RespostaModel.query.filter_by(
        chamado_id=chamado_id
    ).order_by(RespostaModel.criado_em.asc()).all()


def deletar_resposta(id):
    resposta = RespostaModel.query.get(id)
    if resposta:
        db.session.delete(resposta)
        db.session.commit()
        return True
    return False
