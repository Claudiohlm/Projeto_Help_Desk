# camada de servico do usuario
from ..models.usuario_model import UsuarioModel
from src import db


# cadastrar usuario a partir de um objeto ja montado (com senha e tipo definidos)
def cadastrar_usuario_obj(usuario_db):
    db.session.add(usuario_db)
    db.session.commit()
    return usuario_db


# versao antiga (mantida por compatibilidade, caso algo use)
def cadastrar_usuario(usuario):
    usuario_db = UsuarioModel(nome=usuario.nome, email=usuario.email, senha=usuario.senha)
    usuario_db.gen_senha(usuario.senha)
    db.session.add(usuario_db)
    db.session.commit()
    return usuario_db


def listar_usuario():
    return UsuarioModel.query.all()


def listar_usuario_id(id):
    return UsuarioModel.query.get(id)


def listar_usuario_email(email):
    return UsuarioModel.query.filter_by(email=email).first()


def deletar_usuario(id):
    usuario = UsuarioModel.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return True
    return False


def editar_usuario(id, novo_usuario):
    usuario = UsuarioModel.query.get(id)
    if usuario:
        usuario.nome = novo_usuario['nome']
        usuario.email = novo_usuario['email']
        if novo_usuario.get('senha'):
            usuario.gen_senha(novo_usuario['senha'])
        db.session.commit()
        return usuario
    return None
