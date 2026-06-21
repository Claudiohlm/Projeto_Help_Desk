# criar o modelo do banco de dados para as tabelas de chamado e resposta
from src import db
from datetime import datetime


class ChamadoModel(db.Model):
    __tablename__ = "chamado"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(80), nullable=True)
    prioridade = db.Column(db.String(20), nullable=False, default="media")  # baixa, media, alta, critica
    status = db.Column(db.String(20), nullable=False, default="aberto")     # aberto, em_atendimento, resolvido, fechado
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relacionamento: um chamado tem muitas respostas
    respostas = db.relationship(
        "RespostaModel",
        backref="chamado",
        cascade="all, delete-orphan",
        lazy=True
    )


class RespostaModel(db.Model):
    __tablename__ = "resposta"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mensagem = db.Column(db.Text, nullable=False)
    chamado_id = db.Column(db.Integer, db.ForeignKey("chamado.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
