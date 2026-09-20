uv init . → cria o pyproject.toml (registro do projeto e das dependências)
uv venv --python 3.13 → cria o ambiente Python isolado (.venv/)
source .venv/bin/activate → liga esse ambiente no terminal
uv add fastapi uvicorn sqlalchemy alembic "psycopg[binary]" ipykernel
uv sync python-dotenv pandas

fastapi — o framework que define a API: as rotas (/alunos, /disciplinas...), o que cada uma recebe e devolve.
uvicorn — o servidor que roda a API de verdade. O FastAPI sozinho é só código; o uvicorn é quem "liga" e deixa ela respondendo em localhost:8000.
sqlalchemy — o ORM: transforma suas classes Python (models.py) em tabelas e consultas SQL, sem você escrever SQL na mão.
alembic — gerencia as migrations: cria/altera as tabelas no banco conforme os models mudam, e guarda esse histórico de mudanças.
psycopg2-binary — o driver de conexão especificamente com o Postgres. Cada banco (Postgres, MySQL...) precisa de um driver diferente pro SQLAlchemy conseguir falar com ele.
python-dotenv — lê o arquivo .env e carrega as variáveis (tipo a URL do banco) pro código, sem deixar isso fixo/exposto no código-fonte.
pandas — manipula os resultados do banco como tabelas (DataFrame), útil pra transformar isso em JSON de resposta da API.

!!!
uv sync - instala tudo que está no pyproject.toml (usado ao clonar em outra máquina)

ir no dbeaver e criar data base ou CREATE DATABASE fastapi_orm_db


.env: user=aninha
senha=1234
host=localhost
port=5432
banco=fastapi_orm_db

database.py- configuração de conexão com o banco
main.py
models.py-as tabelas no formato de ORM 
schemas.py-esqueletos das validações das informações de entrada e saída

alembic init alembic 
alembic revision --autogenerate
alembic upgrade head

uv run uvicorn app.main:app --reload