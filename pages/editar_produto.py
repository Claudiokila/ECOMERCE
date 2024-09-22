import streamlit as st
import pandas as pd

# Função para carregar produtos do CSV
def carregar_produtos():
    try:
        return pd.read_csv("produtos.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["id", "nome", "preco", "descricao", "quantidade", "imagem"])

# Função para salvar produtos no CSV
def salvar_produtos(produtos):
    produtos.to_csv("produtos.csv", index=False)

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
                    caminho_imagem = os.path.join("imagens", imagem.name)
                    with open(caminho_imagem, "wb") as f:
                        f.write(imagem.getbuffer())
                    produtos.loc[produtos['id'] == produto_info['id'], 'imagem'] = imagem.name

                salvar_produtos(produtos)
                st.success(f"Produto '{nome}' atualizado com sucesso!")

if __name__ == "__main__":
    editar_produto()
