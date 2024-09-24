import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageOps  # Biblioteca Pillow para manipulação de imagens

# Configuração padrão para o modo wide
st.set_page_config(layout="wide")

# Função para carregar produtos de um arquivo CSV
def carregar_produtos():
    return pd.read_csv("produtos.csv")

# Função para redimensionar as imagens
def redimensionar_imagem(caminho_imagem, largura_padrao=400, altura_padrao=400):
    imagem = Image.open(caminho_imagem)
    imagem_redimensionada = imagem.resize((largura_padrao, altura_padrao))  # Redimensiona para um tamanho fixo
    return imagem_redimensionada

# Função para arredondar bordas da imagem
def bordas_arredondadas(imagem, porcentagem_raio=25):
    largura, altura = imagem.size
    raio = int(min(largura, altura) * porcentagem_raio / 100)  # Calcula o raio com base na porcentagem

    # Criar uma máscara de imagem com bordas arredondadas
    mask = Image.new('L', (largura, altura), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (largura, altura)], radius=raio, fill=255)

    # Aplicar a máscara à imagem
    imagem_arredondada = ImageOps.fit(imagem, (largura, altura))
    imagem_arredondada.putalpha(mask)

    return imagem_arredondada

# Função para exibir produtos e permitir adicionar/remover do carrinho
def loja_virtual():
    # CSS para layout simples
    
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;500;700&display=swap');
        .main {{
            background-color: #1A3680; /* Cor de fundo */
            font-family: 'Roboto', sans-serif; /* Fonte moderna */
        }}
        header {{
            background-color: #E50320;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.1); /* Sombra leve */
            text-align: center;
        }}
        h1 {{
            color: white;
            text-align: center;
            font-size: 3em;
        }}
        h2, h3, p {{
            color: white;
        }}
        .stButton > button {{
            background-color: #E50320;
            color: white;
            border-radius: 10px;
            transition: background-color 0.3s ease;
            padding: 10px;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
        }}
        .stButton > button:hover {{
            background-color: #1877F2;
        }}
        .item-carrinho {{
            background-color: #789899;
            color: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
            transition: background-color 0.3s ease;
        }}
        .item-carrinho:hover {{
            background-color: #1877F2;
        }}

        /* Linha simples para separar produtos */
        .linha-futurista {{
            width: 100%;
            height: 3px;
            background: linear-gradient(to right, #E50320, #1A3680);
            margin: 30px 0;
            border-radius: 5px;
        }}

        /* Bordas arredondadas nas imagens */
        .produto-imagem img {{
            border-radius: 25%; /* Borda arredondada de 25% */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    # Seção de ícones
    st.markdown(
        """
        <div class="icon">
            <i class="fas fa-magnifying-glass" onclick="alert('Buscar funcionalidade não implementada');"></i>
            <i class="fas fa-heart" onclick="alert('Favoritos funcionalidade não implementada');"></i>
            <i class="fas fa-cart-shopping" onclick="alert('Carrinho funcionalidade não implementada');"></i>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Título da loja
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
            imagem_produto = produto['imagem']
            caminho_imagem = f"imagens/{imagem_produto}"  # Caminho para as imagens
            imagem_redimensionada = redimensionar_imagem(caminho_imagem)  # Redimensiona a imagem
            imagem_com_bordas = bordas_arredondadas(imagem_redimensionada, porcentagem_raio=25)  # Adiciona bordas arredondadas
            # Exibir a imagem no Streamlit
            st.image(imagem_com_bordas)

        with col2:
            st.markdown(f"<h3>{produto['nome']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p>Preço: R$ {produto['preco']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>Descrição: {produto['descricao']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>Quantidade disponível: {produto['quantidade']}</p>", unsafe_allow_html=True)

            # Organizando o input de quantidade e botão em colunas menores
            col_qtd, col_btn = st.columns([1, 3])
            with col_qtd:
                quantidade = st.number_input(f"", min_value=1, max_value=produto['quantidade'], step=1, key=f"quantidade_{produto['id']}", label_visibility="collapsed")
            with col_btn:
                if st.button(f"Adicionar {produto['nome']} ao carrinho", key=f"adicionar_{produto['id']}"):
                    adicionar_ao_carrinho(produto, quantidade)
                    st.success(f"{quantidade} unidade(s) de {produto['nome']} adicionada(s) ao carrinho.")

        # Adicionar a linha entre os produtos
        st.markdown('<div class="linha-futurista"></div>', unsafe_allow_html=True)

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
