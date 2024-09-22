import streamlit as st 
import pandas as pd
import os

# Função para carregar produtos do CSV
def carregar_produtos():
    try:
        return pd.read_csv("../produtos.csv")  # Caminho atualizado
    except FileNotFoundError:
        return pd.DataFrame(columns=["id", "nome", "preco", "descricao", "quantidade", "imagem"])

# Função para salvar produtos no CSV
def salvar_produtos(produtos):
    produtos.to_csv("../produtos.csv", index=False)  # Caminho atualizado

# Função para cadastrar novos produtos
def cadastrar_produto():
    st.title("Cadastro de Produtos")

    nome = st.text_input("Nome do produto")
    preco = st.number_input("Preço", min_value=0.0, format="%.2f")
    descricao = st.text_area("Descrição do produto")
    quantidade = st.number_input("Quantidade", min_value=1, step=1)
    imagem = st.file_uploader("Carregar imagem do produto", type=["jpg", "png", "jpeg"])

    if st.button("Cadastrar Produto"):
        if not nome or preco <= 0 or not descricao or quantidade <= 0 or imagem is None:
            st.error("Todos os campos são obrigatórios!")
        else:
            produtos = carregar_produtos()
            novo_id = produtos['id'].max() + 1 if not produtos.empty else 1
            pasta_imagens = "../imagens/"  # Caminho atualizado
            if not os.path.exists(pasta_imagens):
                os.makedirs(pasta_imagens)

            caminho_imagem = os.path.join(pasta_imagens, imagem.name)
            with open(caminho_imagem, "wb") as f:
                f.write(imagem.getbuffer())

            novo_produto = pd.DataFrame({
                "id": [novo_id],
                "nome": [nome],
                "preco": [preco],
                "descricao": [descricao],
                "quantidade": [quantidade],
                "imagem": [imagem.name]
            })

            produtos = pd.concat([produtos, novo_produto], ignore_index=True)
            salvar_produtos(produtos)
            st.success(f"Produto '{nome}' cadastrado com sucesso!")

# Função para editar produtos
def editar_produto():
    st.title("Editar Produto")
    produtos = carregar_produtos()
    
    produto_selecionado = st.selectbox("Selecionar produto", produtos['nome'].tolist())

    if produto_selecionado:
        produto_info = produtos[produtos['nome'] == produto_selecionado].iloc[0]

        nome = st.text_input("Nome do produto", value=produto_info['nome'])
        preco = st.number_input("Preço", min_value=0.0, value=float(produto_info['preco']), format="%.2f")
        descricao = st.text_area("Descrição do produto", value=produto_info['descricao'])
        quantidade = st.number_input("Quantidade", min_value=1, value=int(produto_info['quantidade']), step=1)

        imagem = st.file_uploader("Carregar nova imagem do produto (deixe em branco para não alterar)", type=["jpg", "png", "jpeg"])

        if st.button("Atualizar Produto"):
            if not nome or preco <= 0 or not descricao or quantidade <= 0:
                st.error("Todos os campos são obrigatórios!")
            else:
                produtos.loc[produtos['id'] == produto_info['id'], ['nome', 'preco', 'descricao', 'quantidade']] = [nome, preco, descricao, quantidade]

                if imagem is not None:
                    caminho_imagem = os.path.join("../imagens", imagem.name)  # Caminho atualizado
                    with open(caminho_imagem, "wb") as f:
                        f.write(imagem.getbuffer())
                    produtos.loc[produtos['id'] == produto_info['id'], 'imagem'] = imagem.name

                salvar_produtos(produtos)
                st.success(f"Produto '{nome}' atualizado com sucesso!")

if __name__ == "__main__":
    cadastrar_produto()
    editar_produto()
