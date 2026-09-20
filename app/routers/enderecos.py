from fastapi import FastAPI, APIRouter
import pandas as pd
from app.database import engine
from app.schemas import EnderecoIn, EnderecoUpdateIn
from sqlalchemy import text

router = APIRouter(prefix="/enderecos")

@router.get("/pegar-mensagem")
def primeira_api():
    return {"message": "Hello World"}


@router.get("/pegar-dados-endereco")
def pegar_dados_endereco():
    query = "SELECT * FROM tb_enderecos"
    df = pd.read_sql(query, engine)
    df = df.astype(object).where(pd.notnull(df), None)
    return df.to_dict(orient="records")

@router.post("/criar-endereco")
def criar_endereco(endereco: EnderecoIn):
    # Transformando dict em df
    df = pd.DataFrame([endereco.model_dump()])
    # Insert no banco de dados
    df.to_sql("tb_enderecos", engine, if_exists="append", index=False)
    return {"mensagem": "Endereço cadastrado com sucesso!"}

@router.delete("/deletar-endereco/{id}")
def deletar_endereco(id: int):
    query = "DELETE FROM tb_enderecos WHERE id = :id"
    with engine.connect() as conn:
        conn.execute(text(query), {"id": id})
        conn.commit()
    return {"mensagem": "Endereço deletado com sucesso!"}

@router.put("/atualizar-endereco/{id}")
def atualizar_endereco(id: int, endereco: EnderecoUpdateIn):
    # pega só os campos que foram enviados
    dados = endereco.model_dump(exclude_unset=True)
    # monta o SET dinamicamente (ex: "bairro = :bairro, cidade = :cidade")
    campos_sql = ", ".join([f"{chave} = :{chave}" for chave in dados.keys()])
    query = f"UPDATE tb_enderecos SET {campos_sql} WHERE id = :id"
    with engine.connect() as conn:
        conn.execute(text(query), {"id": id, **dados})
        conn.commit()
    return {"mensagem": "Endereço atualizado com sucesso!"}