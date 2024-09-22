import pandas as pd
import streamlit as st
import plotly.express as px

# Carregar produtos do CSV
def carregar_produtos():
    return pd.read_csv("produtos.csv")

# Simulando dados do carrinho (aqui você pode integrar com a lógica do seu carrinho)
def carregar_carrinho():
    return [
        {"id": 1, "nome": "Camiseta", "preco": 49.99, "quantidade": 2},
        {"id": 2, "nome": "Calça Jeans", "preco": 79.90, "quantidade": 1},
        {"id": 4, "nome": "Jaqueta", "preco": 199.90, "quantidade": 1},
    ]

# Função para gerar resumo
def gerar_resumo():
    produtos = carregar_produtos()
    carrinho = carregar_carrinho()

    # Produtos no carrinho
    df_carrinho = pd.DataFrame(carrinho)

    # Produtos vendidos (exemplo, aqui você poderia integrar com uma base real)
    produtos_vendidos = df_carrinho.groupby('nome').sum().reset_index()

    # Produtos mais comprados
    produtos_mais_comprados = df_carrinho.groupby('nome').sum().reset_index().sort_values(by='quantidade', ascending=False)

    # Produtos com estoque baixo (definindo estoque baixo como menos de 5 unidades)
    produtos_estoque_baixo = produtos[produtos['quantidade'] < 5]

    return df_carrinho, produtos_vendidos, produtos_mais_comprados, produtos_estoque_baixo

# Função principal para exibir os resumos
def app():
    st.title("Resumo de Produtos")

    df_carrinho, produtos_vendidos, produtos_mais_comprados, produtos_estoque_baixo = gerar_resumo()

    # Layout em colunas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Produtos no Carrinho")
        st.dataframe(df_carrinho)

        st.subheader("Produtos Vendidos")
        st.dataframe(produtos_vendidos)

    with col2:
        st.subheader("Produtos Mais Comprados")
        st.dataframe(produtos_mais_comprados)

        st.subheader("Produtos com Estoque Baixo")
        st.dataframe(produtos_estoque_baixo)

    # Gráficos
    st.subheader("Gráficos de Resumo")

    # Gráfico de Pizza
    fig_pizza = px.pie(produtos_vendidos, values='quantidade', names='nome', title='Distribuição de Produtos Vendidos')
    st.plotly_chart(fig_pizza)

    # Gráfico de Barras
    fig_barras = px.bar(produtos_mais_comprados, x='nome', y='quantidade', title='Produtos Mais Comprados', color='quantidade')
    st.plotly_chart(fig_barras)

    # Gráfico Linear
    fig_linear = px.line(produtos_mais_comprados, x='nome', y='quantidade', title='Tendência de Compras')
    st.plotly_chart(fig_linear)

if __name__ == "__main__":
    app()
