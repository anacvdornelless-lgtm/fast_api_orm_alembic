from app.schemas import NotaIn, NotaUpdateIn
from fastapi import FastAPI, APIRouter
from sqlalchemy import create_engine, text
import pandas as pd
from typing import Optional
from pydantic import BaseModel 
from app.database import engine


router = APIRouter(prefix="/notas")


@router.get("/pegar-mensagem")
def primeira_api():
    return {"message": "rotas notas"}


@router.get("/pegar-dados-notas")
def pegar_dados_notas():
    query = "SELECT * FROM tb_notas"
    df = pd.read_sql(query, engine)
    df = df.astype(object).where(pd.notnull(df), None)
    return df.to_dict(orient="records")


@router.get("/pegar-dados-notas-por-id/{id}")
def pegar_dados_notas_por_id(id: int):
    query = text("SELECT * FROM tb_notas WHERE id = :id")
    df = pd.read_sql(query, engine, params={"id": id})
    df = df.astype(object).where(pd.notnull(df), None)
    return df.to_dict(orient="records")


@router.post("/criar-nota")
def criar_nota(nota: NotaIn):
    # Transformando dict em df
    df = pd.DataFrame([nota.model_dump()])
    # Insert no banco de dados
    df.to_sql("tb_notas", engine, if_exists="append", index=False)
    return {"mensagem": "Nota cadastrada com sucesso!"}


@router.put("/atualizar-nota/{id}")
def atualizar_nota(id: int, nota: NotaUpdateIn):
    # pega só os campos que foram enviados
    dados = nota.model_dump(exclude_unset=True)
    # monta o SET dinamicamente (ex: "nota = :nota")
    campos_sql = ", ".join([f"{chave} = :{chave}" for chave in dados.keys()])
    query = f"UPDATE tb_notas SET {campos_sql} WHERE id = :id"
    with engine.connect() as conn:
        conn.execute(text(query), {"id": id, **dados})
        conn.commit()
    return {"mensagem": "Nota atualizada com sucesso!"}


@router.delete("/deletar-nota/{id}")
def deletar_nota(id: int):
    query = "DELETE FROM tb_notas WHERE id = :id"
    with engine.connect() as conn:
        conn.execute(text(query), {"id": id})
        conn.commit()
    return {"mensagem": "Nota deletada com sucesso!"}