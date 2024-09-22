import streamlit as st
import pandas as pd

# Função para carregar produtos do CSV
def carregar_produtos():
    try:
        return pd.read_csv("produtos.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["id", "nome", "preco", "descricao", "quantidade", "imagem"])

# Função para visualizar estoque
def visualizar_estoque():
    st.title("Visualizar Estoque")
    produtos = carregar_produtos()
    
    if not produtos.empty:
        for index, produto in produtos.iterrows():
            st.markdown(f"**{produto['nome']}**")
            st.markdown(f"Preço: R$ {produto['preco']:.2f}")
            st.markdown(f"Quantidade: {produto['quantidade']}")
            st.markdown(f"Descrição: {produto['descricao']}")
            st.image(f"imagens/{produto['imagem']}", width=150)
            st.markdown("---")
    else:
        st.warning("Nenhum produto cadastrado.")

if __name__ == "__main__":
    visualizar_estoque()
