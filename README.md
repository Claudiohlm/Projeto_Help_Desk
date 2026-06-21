# 🎫 Projeto HelpDesk — Sistema de Suporte Técnico

API REST para gerenciamento de chamados de suporte técnico, com interface web,
sistema de autenticação e níveis de permissão.

**Disciplina:** Sistemas de Informação — 8º Semestre (2026)
**Autor:** Claudio Henrique de Lima Melo
**Repositório:** https://github.com/Claudiohlm/Projeto_Help_Desk

---

## 📋 Sobre o negócio

O **HelpDesk** é um sistema de suporte técnico onde usuários abrem chamados
descrevendo problemas (de hardware ou software) e a equipe de atendimento
acompanha e resolve cada solicitação. O modelo replica o núcleo de plataformas
reais como **Zendesk** e **Freshdesk**, amplamente usadas por empresas de TI.

### Problema que resolve
Sem um sistema dedicado, as solicitações de suporte chegam de forma
desorganizada (e-mail, mensagens, verbalmente), sem controle de prioridade,
histórico ou status. O HelpDesk centraliza tudo isso em um fluxo organizado.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Função |
|------------|--------|
| Python 3 | Linguagem principal |
| Flask | Framework web / API REST |
| Flask-RESTful | Estruturação dos endpoints (classes Resource) |
| Flask-SQLAlchemy | ORM — mapeamento objeto-relacional |
| Flask-Migrate (Alembic) | Versionamento e migração do banco |
| Marshmallow | Validação e serialização (schemas) |
| Passlib (argon2) | Criptografia de senhas |
| PostgreSQL (Aiven) | Banco de dados online na nuvem |
| Bootstrap 5 | Interface web responsiva |
| python-dotenv | Variáveis de ambiente |

---

## 🗂️ Estrutura do projeto

```
Projeto_Help_Desk/
├── app.py                      # Ponto de entrada da aplicação
├── connection.py               # Configuração da conexão com o banco
├── criar_admin.py              # Script que cria o administrador de fábrica
├── requirements.txt            # Dependências do projeto
├── migrations/                 # Migrations do banco (Alembic)
└── src/
    ├── __init__.py             # Configuração do Flask e blueprints
    ├── models/                 # Camada Model (tabelas)
    │   ├── usuario_model.py
    │   └── chamado_model.py
    ├── schemas/                # Camada Schema (validação)
    │   ├── usuario_schema.py
    │   └── chamado_schema.py
    ├── services/               # Camada Service (regras de negócio)
    │   ├── usuario_service.py
    │   └── chamado_service.py
    ├── views/                  # Camada View (endpoints)
    │   ├── usuario_view.py
    │   ├── chamado_view.py
    │   ├── login_view.py
    │   └── web_view.py
    └── templates/
        └── index.html          # Interface web (Bootstrap)
```

---

## 🗄️ Modelagem do banco de dados

### Tabela `usuario`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer (PK) | Identificador |
| nome | String(120) | Nome do usuário |
| email | String(120) UNIQUE | E-mail (login) |
| senha | String(255) | Senha criptografada (argon2) |
| tipo | String(20) | `admin` ou `comum` |

### Tabela `chamado`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer (PK) | Identificador |
| titulo | String(200) | Título do chamado |
| descricao | Text | Descrição do problema |
| categoria | String(80) | hardware ou software |
| prioridade | String(20) | Definida automaticamente pela categoria |
| status | String(20) | aberto / em_atendimento / resolvido / fechado |
| usuario_id | Integer (FK) | Quem abriu o chamado |
| criado_em | DateTime | Data de criação |
| atualizado_em | DateTime | Última atualização |

### Tabela `resposta`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer (PK) | Identificador |
| mensagem | Text | Conteúdo da resposta |
| chamado_id | Integer (FK) | Chamado relacionado |
| usuario_id | Integer (FK) | Quem respondeu |
| criado_em | DateTime | Data da resposta |

### Relacionamentos
```
usuario (1) ───< (N) chamado
chamado (1) ───< (N) resposta
```

---

## 📜 Regras de negócio

1. **Prioridade automática:** o usuário não escolhe a prioridade. O sistema
   define pela categoria — `software` → alta, `hardware` → média.
2. **Status inicial:** todo chamado nasce como `aberto`.
3. **Transição automática:** ao receber a primeira resposta, o chamado muda
   automaticamente de `aberto` para `em_atendimento`.
4. **Chamado fechado é imutável:** não aceita alteração de status nem novas
   respostas.
5. **Permissão de visualização:** usuário `comum` vê apenas os chamados que
   ele criou; `admin` vê todos.
6. **Permissão de status:** apenas `admin` pode alterar o status de um chamado.
7. **Exclusão em cascata:** ao deletar um chamado, suas respostas são removidas.

---

## 🔌 Endpoints da API

### Autenticação
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/login` | Autentica usuário (verifica senha criptografada) |

### Usuários
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/usuarios` | Lista todos os usuários |
| GET | `/usuarios/<id>` | Busca usuário por ID |
| POST | `/usuarios` | Cadastra usuário (sempre tipo comum) |
| DELETE | `/usuarios/<id>` | Remove usuário |

### Chamados
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/chamados` | Lista chamados (filtra por permissão) |
| GET | `/chamados/<id>` | Detalha chamado + respostas |
| POST | `/chamados` | Abre novo chamado |
| PUT | `/chamados/<id>` | Muda status (apenas admin) |
| DELETE | `/chamados/<id>` | Remove chamado |

### Respostas
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/chamados/<id>/respostas` | Lista respostas de um chamado |
| POST | `/chamados/<id>/respostas` | Adiciona resposta |
| DELETE | `/respostas/<id>` | Remove resposta |

---

## ▶️ Como rodar o projeto

### 1. Clonar e entrar na pasta
```bash
git clone https://github.com/Claudiohlm/Projeto_Help_Desk.git
cd Projeto_Help_Desk
```

### 2. Criar e ativar o ambiente virtual
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar o arquivo `.env`
Crie um arquivo `.env` na raiz com:
```env
DATABASE_URL=postgresql://usuario:senha@host:porta/banco?sslmode=require
ADMIN_NOME=Administrador
ADMIN_EMAIL=admin@admin.com
ADMIN_SENHA=suaSenhaSecreta
```

### 5. Criar as tabelas
```bash
flask db upgrade
```

### 6. Criar o administrador
```bash
python criar_admin.py
```

### 7. Rodar o servidor
```bash
flask run
```

### 8. Acessar
- Interface web: `http://127.0.0.1:5000/`
- API: `http://127.0.0.1:5000/chamados`

---

## 💻 Interface Web

Além da API, o projeto conta com uma interface web em Bootstrap que consome
os próprios endpoints. Funcionalidades:

- **Login e cadastro** de usuários (com bloqueio por senha incorreta)
- **Abertura de chamados** com prioridade automática
- **Listagem filtrada** por permissão (comum vê os seus, admin vê todos)
- **Respostas** e **mudança de status** (status apenas para admin)
- **Exclusão** de chamados

---

## 🔐 Segurança

- Senhas armazenadas com criptografia **argon2** (nunca em texto puro)
- Credenciais e dados sensíveis mantidos em variáveis de ambiente (`.env`),
  fora do controle de versão
- Conta de administrador provisionada por script controlado (não pelo
  cadastro público)

> **Nota técnica:** as permissões são aplicadas no backend com base no tipo
> do usuário. Em um ambiente de produção, o próximo passo seria implementar
> autenticação por token (JWT) para que as permissões não dependam de
> informação enviada pelo cliente.

---

## ✅ Requisitos atendidos

**Exigidos pelo trabalho:**
- [x] Definição de negócio (HelpDesk)
- [x] Modelagem de novas tabelas (chamado, resposta)
- [x] Model, Schema, Service e View das novas tabelas
- [x] Migrations
- [x] Configuração dos endpoints
- [x] Testes da API
- [x] Código funcional no GitHub
- [x] Documentação

**Extras implementados:**
- [x] Interface web responsiva (Bootstrap)
- [x] Sistema de login com senha criptografada
- [x] Níveis de permissão (admin / comum)
- [x] Prioridade automática por categoria
- [x] Boas práticas de segurança (variáveis de ambiente)
