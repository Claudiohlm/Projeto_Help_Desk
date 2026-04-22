# configuracao das bibliotecas externas/dependecias
# instanciar aqui e configurar
# configurar a connection para apontar para o confiig object do flask

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config.from_object('connection')

db = SQLAlchemy(app)

migrate = Migrate(app, db)
ma = Marshmallow(app)





# TODO : Apontar os modelos criados para a orm conseguir criar as tabelas

from .models.usuario_model import UsuarioModel


# TODO: Apontar quem são as minhas views

#from .views.usuario_view import ViewUsuario