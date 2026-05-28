# criar as rotas da API, camada que recebe as requisicoes
from ..models.usuario_model import UsuarioModel
from ..schemas.usuario_schema import UsuarioSchema
from flask import jsonify
from src import db

# cadastrar usuario
def cadastrar_usuario(usuario):
    usuario_db = UsuarioModel(nome=usuario.nome, email=usuario.email, senha=usuario.senha)
    usuario_db.gen_senha(usuario.senha)
    db.session.add(usuario_db)
    db.session.commit()
    return usuario_db

# listar todos usuarios
def listar_usuario():
    return UsuarioModel.query.all()


# listar usuario por id
def listar_usuario_id(id):
    usuario_encontrado = UsuarioModel.query.get(id)
    return usuario_encontrado
 

# listar usuario por email
def listar_usuario_email(email):
    return UsuarioModel.query.filter_by(email=email).first()

# deletar usuario
def deletar_usuario(id):
    usuario = UsuarioModel.query.get(id)
    if usuario:
        # se verdadeiro
        db.session.delete(usuario)
        db.session.commit()
        return True
    return False


# editar usuario
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