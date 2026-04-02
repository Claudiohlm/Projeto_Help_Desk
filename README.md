# SGU_8_SEMESTRE

Projeto de sistema web em Flask com estrutura preparada para aplicação Python e modelagem de banco de dados.

## Visão geral

Este repositório contém a base de um sistema Flask com dependências listadas em `requirements.txt` e o modelo de banco de dados em `DB/modelagem.mwb`.

## Arquitetura do projeto

- `src/`
  - Diretório de código-fonte da aplicação Flask.
  - Atualmente está vazio no repositório, mas daqui deve vir a aplicação principal, modelos, rotas e configuração.
- `DB/modelagem.mwb`
  - Arquivo de modelagem MySQL Workbench do banco de dados do sistema.
- `requirements.txt`
  - Lista de dependências Python para o projeto.
- `.env.example`
  - Exemplo de variáveis de ambiente necessárias para conexão com o banco de dados.
- `.gitignore`
  - Arquivos e pastas ignorados pelo Git.

## Tecnologias usadas

- Python
- Flask 3.x
- Jinja2
- Werkzeug
- Click
- Blinker
- itsdangerous

## Instalação

1. Criar e ativar ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instalar dependências:

```bash
pip install -r requirements.txt
```

## Configuração

Copie o arquivo `.env.example` para `.env` e preencha os valores do banco de dados:

```env
DB_NAME='nome_do_banco'
DB_USER='usuario'
DB_HOST='localhost'
DB_PASSWORD='senha'
```

## Banco de dados

- Importe ou abra `DB/modelagem.mwb` no MySQL Workbench para visualizar e gerar o esquema do banco.
- Use as credenciais definidas em `.env` para conectar a aplicação ao banco de dados.

## Execução

A partir da raiz do projeto, execute a aplicação Flask usando o arquivo principal em `src/` quando ele estiver disponível.

Exemplo genérico:

```bash
export FLASK_APP=src/app.py
export FLASK_ENV=development
flask run
```

ou

```bash
python src/app.py
```

## Observações

- A pasta `src/` está preparada para receber o código-fonte da aplicação.
- Caso queira iniciar o projeto, adicione o ponto de entrada Flask em `src/app.py` e mantenha a modelagem de banco em `DB/modelagem.mwb`.

