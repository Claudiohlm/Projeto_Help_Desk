# criar o modelo do banco de dados para a tabela de usuario
from src import db
from passlib.context import CryptContext


class UsuarioModel(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    # tipo do usuario: "admin" pode ver/gerenciar todos os chamados,
    # "comum" so ve e gerencia os proprios chamados
    tipo = db.Column(db.String(20), nullable=False, default="comum")

    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def gen_senha(self, senha):
        self.senha = self.pwd_context.hash(senha)

    def verifica_senha(self, senha):
        return self.pwd_context.verify(senha, self.senha)
