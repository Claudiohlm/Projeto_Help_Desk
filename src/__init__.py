from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restful import Api

# template_folder aponta para a pasta templates dentro de src
app = Flask(__name__, template_folder='templates')
app.config.from_object('connection')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
api = Api(app)

# models
from .models.usuario_model import UsuarioModel
from .models.chamado_model import ChamadoModel, RespostaModel

# views da API
from .views import usuario_view
from .views import chamado_view
from .views import login_view      # NOVO - rota de login

# view da interface web
from .views.web_view import web_bp  # NOVO - paginas HTML
app.register_blueprint(web_bp)      # NOVO