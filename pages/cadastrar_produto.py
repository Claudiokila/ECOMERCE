import streamlit as st
import pandas as pd
import sqlite3

CAMINHO_DB = 'banco.db'


# Função para carregar produtos do banco de dados
def carregar_produtos(caminho_db=CAMINHO_DB):
    with sqlite3.connect(caminho_db) as conn:
        df = pd.read_sql_query("SELECT * FROM PRODUTOS", conn)
    return df

# Função para salvar produtos no banco de dados
def salvar_produtos(dataframe, caminho_db=CAMINHO_DB):
    with sqlite3.connect(caminho_db) as conn:
        dataframe.to_sql('PRODUTOS', conn, if_exists='replace', index=False)

# Função para cadastrar novos produtos
def cadastrar_produto():
    st.title("Cadastro de Produtos")

    cod_barra = st.number_input("Código de Barras", min_value=0, step=1)
    produto = st.text_input("Nome do Produto", max_chars=18)
    descricao = st.text_area("Descrição do Produto", max_chars=20)
    imagem = st.file_uploader("Carregar Imagem do Produto", type=["jpg", "png", "jpeg"])
    estoque = st.number_input("Quantidade em Estoque", min_value=0, step=1)
    preco_compra = st.number_input("Preço de Compra", min_value=0.0, format="%.2f")
    preco_venda = st.number_input("Preço de Venda", min_value=0.0, format="%.2f")
    margem = preco_venda - preco_compra

    if st.button("Cadastrar Produto"):
        if not produto or not descricao or estoque < 0 or preco_compra <= 0 or preco_venda <= 0 or margem < 0 or imagem is None:
            st.error("Todos os campos são obrigatórios!")
        else:
            produtos = carregar_produtos()
            novo_id = produtos['ID'].max() + 1 if not produtos.empty else 1
            
            # Ler a imagem em bytes
            imagem_bytes = imagem.getvalue()

            novo_produto = pd.DataFrame({
                "ID": [novo_id],
                "COD_BARRA": [cod_barra],
                "PRODUTO": [produto],
                "DESCRICAO": [descricao],
                "IMAGEM": [imagem_bytes],
                "ESTOQUE": [estoque],
                "PRECO_COMPRA": [preco_compra],
                "PRECO_VENDA": [preco_venda],
                "MARGEM": [margem]
            })

            produtos = pd.concat([produtos, novo_produto], ignore_index=True)
            salvar_produtos(produtos)
            st.success(f"Produto '{produto}' cadastrado com sucesso!")

if __name__ == "__main__":
    cadastrar_produto()
