# =============================================================
# SCRIPT: criar_admin.py
# Cria o usuario administrador de fabrica.
# A senha agora vem do arquivo .env (nao fica exposta no codigo).
# RODE UMA VEZ:  python criar_admin.py
# =============================================================

import os
from dotenv import load_dotenv
from src import app, db
from src.models.usuario_model import UsuarioModel

# carrega as variaveis do .env
load_dotenv()

# le os dados do admin a partir do .env
# (com valores padrao caso nao estejam definidos)
ADMIN_NOME = os.getenv("ADMIN_NOME", "Administrador")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@admin.com")
ADMIN_SENHA = os.getenv("ADMIN_SENHA")

# protecao: nao deixa criar admin sem senha definida no .env
if not ADMIN_SENHA:
    print("❌ ERRO: a variavel ADMIN_SENHA nao foi encontrada no .env")
    print("   Adicione no seu arquivo .env a linha:")
    print("   ADMIN_SENHA=suaSenhaSecreta")
    exit()

with app.app_context():
    existente = UsuarioModel.query.filter_by(email=ADMIN_EMAIL).first()

    if existente:
        print(f"⚠️  O admin '{ADMIN_EMAIL}' ja existe. Nada a fazer.")
    else:
        admin = UsuarioModel(
            nome=ADMIN_NOME,
            email=ADMIN_EMAIL,
            senha="",
            tipo="admin"
        )
        admin.gen_senha(ADMIN_SENHA)
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin criado com sucesso!")
        print(f"   Email: {ADMIN_EMAIL}")
        print("   Senha: (definida no .env)")
        print("   Tipo:  admin")