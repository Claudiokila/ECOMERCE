import sqlite3
import pandas as pd

def adicionar_produto(produto):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO PRODUTOS VALUES (?, ?, ?)", produto)
        conn.commit()

def carregar_produtos():
    with sqlite3.connect('database.db') as conn:
        df = pd.read_sql_query("SELECT * FROM PRODUTOS", conn)
    return df

def atualizar_produto(produto, codigo):
    '''Atualiza um produto no banco de dados, pegando cada valor do dict produto e o código do produto'''
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        '''update com produtos.keys() e produtos.values()'''
        query = f"UPDATE PRODUTOS SET {', '.join([f'{key} = ?' for key in produto.keys()])} WHERE CODIGO = ?"
        cursor.execute(query, list(produto.values()) + [codigo])

def deletar_produto(codigo):
    '''Deleta um produto do banco de dados, passando o código do produto'''
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PRODUTOS WHERE CODIGO = ?", (codigo,))
        conn.commit()
