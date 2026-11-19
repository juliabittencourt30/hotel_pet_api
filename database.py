import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def executar_sql(sql, parametros=()):
    conexao = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    cursor = None

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(sql, parametros)
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        conexao.close()