from flask import Blueprint, render_template

# blueprint que serve a interface web (paginas HTML)
web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    """Pagina principal do sistema HelpDesk."""
    return render_template("index.html")
