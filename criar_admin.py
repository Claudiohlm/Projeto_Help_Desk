# =============================================================
# SCRIPT: criar_admin.py
# Cria o usuario administrador de fabrica.
# RODE UMA VEZ:  python criar_admin.py
# =============================================================

from src import app, db
from src.models.usuario_model import UsuarioModel

# dados do admin de fabrica
ADMIN_NOME = "Administrador"
ADMIN_EMAIL = "admin@admin.com"
ADMIN_SENHA = "admin2026"

with app.app_context():
    # verifica se o admin ja existe (pra nao duplicar)
    existente = UsuarioModel.query.filter_by(email=ADMIN_EMAIL).first()

    if existente:
        print(f"⚠️  O admin '{ADMIN_EMAIL}' ja existe. Nada a fazer.")
    else:
        admin = UsuarioModel(
            nome=ADMIN_NOME,
            email=ADMIN_EMAIL,
            senha="",          # sera preenchida pelo gen_senha abaixo
            tipo="admin"
        )
        admin.gen_senha(ADMIN_SENHA)   # criptografa a senha com argon2
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin criado com sucesso!")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   Senha: {ADMIN_SENHA}")
        print("   Tipo:  admin")
