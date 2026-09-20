from fastapi import FastAPI, APIRouter
from app.schemas import DisciplinaIn, DisciplinaUpdateIn
import pandas as pd
from app.database import engine
from sqlalchemy import text

router = APIRouter(prefix="/disciplinas")

@router.get("/pegar-mensagem")
def primeira_api():
    return {"message": "disciplinas"}

@router.get("/pegar-dados-disciplina")
def pegar_dados_disciplina():
    query = "SELECT * FROM tb_disciplinas"
    df = pd.read_sql(query, engine)
    df = df.astype(object).where(pd.notnull(df), None)
    return df.to_dict(orient="records")

@router.post("/criar-disciplina")
def criar_disciplina(disciplina: DisciplinaIn):
    # Transformando dict em df
    df = pd.DataFrame([disciplina.model_dump()])
    # Insert no banco de dados
    df.to_sql("tb_disciplinas", engine, if_exists="append", index=False)
    return {"mensagem": "Disciplina cadastrada com sucesso!"}

@router.put("/atualizar-disciplina/{id}")
def atualizar_disciplina(id: int, disciplina: DisciplinaUpdateIn):
    # pega só os campos que foram enviados
    dados = disciplina.model_dump(exclude_unset=True)
    # monta o SET dinamicamente (ex: "carga = :carga")
    campos_sql = ", ".join([f"{chave} = :{chave}" for chave in dados.keys()])
    query = f"UPDATE tb_disciplinas SET {campos_sql} WHERE id = :id"
    with engine.connect() as conn:
        conn.execute(text(query), {"id": id, **dados})
        conn.commit()
    return {"mensagem": "Disciplina atualizada com sucesso!"}

@router.delete("/deletar-disciplina/{id}")
def deletar_disciplina(id: int):
    query = "DELETE FROM tb_disciplinas WHERE id = :id"
    with engine.connect() as conn:
        conn.execute(text(query), {"id": id})
        conn.commit()
    return {"mensagem": "Disciplina deletada com sucesso!"}