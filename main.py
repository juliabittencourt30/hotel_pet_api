import logging

from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import JSONResponse
from mysql.connector import Error as MySQLError

from database import executar_sql

app = FastAPI(title="API Hotel Pet")

@app.exception_handler(MySQLError)
def erro_de_banco(request: Request, exc: MySQLError):
    logging.getLogger("uvicorn.error").error("Erro de BD: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro em acesso ao BD"},
    )


def representar_tutores(tutor):
    return {
        "id": tutor["id"],
        "nome": tutor["nome"],
        "telefone": tutor["telefone"]
    }


@app.get("/listartutores")
def listar_tutores():
    sql = "SELECT * FROM tutores"
    tutores = executar_sql(sql)

    return {
        "dados": [representar_tutores(tutor) for tutor in tutores],
        "instrucaosql": {
            "sql": sql,
            "parametros": []
        }
    }


@app.get("/consultartutor/{id}")
def consultar_tutor(id: int = Path(gt=0)):
    sql = "SELECT * FROM tutores WHERE id = %s"
    parametros = (id,)

    tutores = executar_sql(sql, parametros)

    if not tutores:
        raise HTTPException(
            status_code=404,
            detail="Tutor não encontrado."
        )

    return {
        "dados": representar_tutores(tutores[0]),
        "instrucaosql": {
            "sql": sql,
            "parametros": list(parametros)
        }
    }


def representar_pets(pet):
    return {
        "id": pet["id"],
        "nome": pet["nome"],
        "especie": pet["especie"],
        "tutorId": pet["tutorId"]
    }


@app.get("/listarpets")
def listar_pets():
    sql = "SELECT * FROM pets"
    pets = executar_sql(sql)

    return {
        "dados": [representar_pets(pet) for pet in pets],
        "instrucaosql": {
            "sql": sql,
            "parametros": []
        }
    }


@app.get("/consultarpet/{id}")
def consultar_pet(id: int = Path(gt=0)):
    sql = "SELECT * FROM pets WHERE id = %s"
    parametros = (id,)

    pets = executar_sql(sql, parametros)

    if not pets:
        raise HTTPException(
            status_code=404,
            detail="Pet não encontrado."
        )

    return {
        "dados": representar_pets(pets[0]),
        "instrucaosql": {
            "sql": sql,
            "parametros": list(parametros)
        }
    }