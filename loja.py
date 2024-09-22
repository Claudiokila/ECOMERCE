import streamlit as st
import pandas as pd

# Configuração padrão para o modo wide
st.set_page_config(layout="wide")

# Carregar produtos do CSV
def carregar_produtos():
    return pd.read_csv("produtos.csv")

# Função para exibir produtos e permitir adicionar/remover do carrinho
def loja_virtual():
    # CSS para aplicar o background personalizado e cor fixa no botão
    st.markdown(
        f"""
        <style>
        .main {{
            background-color: #1A3680;  /* Cor de fundo para o corpo principal */
        }}
        header {{
            background-color: #E50320;  /* Cor de fundo para o cabeçalho */
            padding: 10px;
        }}
        h1 {{
            color: white;  /* Cor do texto do título principal */
            text-align: center; /* Centraliza o texto */
        }}
        h2, h3, p {{
            color: white;  /* Cor do texto nas outras seções */
        }}
        .stButton > button {{
            background-color: #E50320; /* Cor fixa para os botões */
            color: white;
        }}
        .item-carrinho {{
            background-color: #789899; /* Cor de fundo quando o item está no carrinho */
            color: white;  /* Cor do texto */
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
        }}
        .item-carrinho:hover {{
            background-color: #1877F2; /* Cor de fundo ao passar o mouse no item do carrinho */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Título da loja com a cor de fundo aplicada ao cabeçalho
    st.markdown("<header><h1>FARMÁCIA LÁ DE CASA</h1></header>", unsafe_allow_html=True)

    # Carregar produtos do CSV
    produtos = carregar_produtos()

    # Campo de filtro para buscar produtos pelo nome
    filtro = st.text_input("Buscar produto", key="filtro")
    
    if filtro:
        produtos = produtos[produtos['nome'].str.contains(filtro, case=False)]

    # Carregar ou inicializar o carrinho na sessão
    if 'carrinho' not in st.session_state:
        st.session_state['carrinho'] = []

    # Função para adicionar ao carrinho
    def adicionar_ao_carrinho(produto, quantidade):
        item_carrinho = {
            "produto": produto['nome'],
            "preco": produto['preco'],
            "quantidade": quantidade,
            "id": produto['id']
        }
        st.session_state['carrinho'].append(item_carrinho)

    # Função para remover do carrinho
    def remover_do_carrinho(produto_id):
        st.session_state['carrinho'] = [item for item in st.session_state['carrinho'] if item['id'] != produto_id]
        st.success("Item removido do carrinho.")

    # Função para finalizar compra
    def finalizar_compra():
        if st.session_state['carrinho']:
            st.session_state['carrinho'] = []
            st.success("Compra finalizada com sucesso! Seu carrinho foi esvaziado.")
        else:
            st.warning("Seu carrinho está vazio. Adicione produtos antes de finalizar a compra.")

    # Exibir cada produto com a opção de adicionar ao carrinho
    for index, produto in produtos.iterrows():
        col1, col2 = st.columns([1, 2])
        with col1:
            imagem_produto = produto['imagem']  # Supondo que a coluna da imagem se chama 'imagem'
            st.image(f"imagens/{imagem_produto}", width=150)  # Usando o caminho da imagem do produto
            
        with col2:
            st.markdown(f"<h3>{produto['nome']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p>Preço: R$ {produto['preco']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>Descrição: {produto['descricao']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>Quantidade disponível: {produto['quantidade']}</p>", unsafe_allow_html=True)

            quantidade = st.number_input(f"Quantidade de {produto['nome']}", min_value=1, max_value=produto['quantidade'], step=1, key=f"quantidade_{produto['id']}")

            if st.button(f"Adicionar {produto['nome']} ao carrinho", key=f"adicionar_{produto['id']}"):
                adicionar_ao_carrinho(produto, quantidade)
                st.success(f"{quantidade} unidade(s) de {produto['nome']} adicionada(s) ao carrinho.")

    # Exibir carrinho
    if st.session_state['carrinho']:
        st.markdown("<h2>Carrinho</h2>", unsafe_allow_html=True)
        total = 0
        for item in st.session_state['carrinho']:
            subtotal = item['preco'] * item['quantidade']
            total += subtotal
            st.markdown(
                f"""
                <div class="item-carrinho">
                    <p>{item['quantidade']}x {item['produto']} - R$ {subtotal:.2f}</p>
                    <p>Preço unitário: R$ {item['preco']:.2f}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if st.button(f"Remover {item['produto']} do carrinho", key=f"remover_{item['id']}"):
                remover_do_carrinho(item['id'])

        st.markdown(f"<h3>Total: R$ {total:.2f}</h3>", unsafe_allow_html=True)
        
        if st.button("Finalizar compra"):
            finalizar_compra()

if __name__ == "__main__":
    loja_virtual()
