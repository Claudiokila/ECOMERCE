import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageOps
from io import BytesIO
import base64
from crud import carregar_produtos

st.set_page_config(layout="wide")

# Função para redimensionar a imagem
def redimensionar_imagem(caminho_imagem, largura_padrao=200, altura_padrao=200):
    imagem = Image.open(caminho_imagem)
    return imagem.resize((largura_padrao, altura_padrao))

# Função para adicionar bordas arredondadas à imagem
def bordas_arredondadas(imagem, porcentagem_raio=25):
    largura, altura = imagem.size
    raio = int(min(largura, altura) * porcentagem_raio / 100)
    mask = Image.new('L', (largura, altura), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (largura, altura)], radius=raio, fill=255)
    imagem_arredondada = ImageOps.fit(imagem, (largura, altura))
    imagem_arredondada.putalpha(mask)
    return imagem_arredondada

# Função para converter imagem para base64
def imagem_para_base64(imagem):
    buffer = BytesIO()
    imagem.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_str

# Função principal da loja virtual
def loja_virtual():
    # Estilos personalizados com CSS para o Streamlit
    st.markdown("""
    <style>
        .stTextInput, .stButton { 
            width: 50%; 
            margin: auto;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: white;
            border: 2px solid #42A5F5;
            border-radius: 25px;
            padding: 5px 10px;
            font-size: 16px;
        }
        .stButton button {
            background-color: #42A5F5;
            color: white;
            border-radius: 25px;
            padding: 10px 20px;
        }
        header { 
            background-color: #1E88E5; 
            padding: 15px; 
            border-radius: 10px; 
        }
        h1 { 
            color: white; 
            text-align: center; 
            font-size: 3em; 
        }
        .card {
            background-color: #E3F2FD;
            border: 2px solid #42A5F5;
            border-radius: 15px;
            padding: 15px;
            margin: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            height: 600px; /* Altura do card ajustada para 600px */
            width: 400px; /* Largura do card ajustada */
        }
        .card img {
            margin-bottom: 15px;
            border-radius: 15px;
            max-width: 100%; /* Garantir que a imagem não ultrapasse a largura do card */
        }
        .card h3 {
            color: #1E88E5;
            margin: 5px 0;
        }
        .card p {
            color: #555;
            margin: 5px 0;
        }
        .add-button {
            background-color: #42A5F5;
            color: white;
            border: none;
            border-radius: 25px;
            padding: 10px 20px;
            cursor: pointer;
            text-align: center;
            width: 100px; /* Largura do botão ajustada para 100px */
            margin-top: auto; /* Para empurrar o botão para o final do card */
        }
        .success-message {
            color: green;
            margin-top: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Cabeçalho
    st.markdown("<header><h1>FARMÁCIA LÁ DE CASA</h1></header>", unsafe_allow_html=True)

    produtos = carregar_produtos()

    # Filtro de busca
    filtro = st.text_input("", placeholder="Digite o nome do produto")

    if st.button("Buscar") and filtro:
        produtos = produtos[produtos['PRODUTO'].str.contains(filtro, case=False)]

    # Inicialização do carrinho
    if 'carrinho' not in st.session_state:
        st.session_state['carrinho'] = []

    # Inicializa a paginação
    if 'pagina' not in st.session_state:
        st.session_state['pagina'] = 0

    # Número de produtos por página e controle de paginação
    produtos_por_pagina = 24  # 8 linhas * 3 colunas
    inicio = st.session_state['pagina'] * produtos_por_pagina
    fim = inicio + produtos_por_pagina

    # Exibindo os produtos em colunas
    num_colunas = 3  # Definindo 3 colunas
    cols = st.columns(num_colunas)  # Criando as colunas

    # Controlar a linha atual
    for index in range(inicio, min(fim, len(produtos))):
        produto = produtos.iloc[index]  # Extrai o produto da tupla
        caminho_imagem = "imagens/salveo.jpg"  # Caminho da imagem do produto
        imagem_redimensionada = redimensionar_imagem(caminho_imagem)
        imagem_com_bordas = bordas_arredondadas(imagem_redimensionada)
        imagem_base64 = imagem_para_base64(imagem_com_bordas)

        # Variável para armazenar mensagem de sucesso
        mensagem_sucesso = ""

        # Usando a coluna atual para exibir o card
        with cols[index % num_colunas]:
            st.markdown(f"""
            <div class="card">
                <img src="data:image/png;base64,{imagem_base64}" alt="Imagem do Produto" width="150">
                <div>
                    <h3>{produto['PRODUTO']}</h3>
                    <p><strong>Preço:</strong> R$ {produto['PRECO_VENDA']}</p>
                    <p><strong>Quantidade disponível:</strong> {produto['ESTOQUE']}</p>
                </div>
                <input type="number" name="quantidade" min="1" max="{produto['ESTOQUE']}" value="1" style="width: 100%; padding: 5px; margin-top: 10px; border-radius: 5px; border: 1px solid #ccc;" required>
                
            </div>
            <p class="success-message" id="success_{index}">{mensagem_sucesso}</p>
            """, unsafe_allow_html=True)

            # Exibindo a lógica do botão "Adicionar"
            if st.button(f"Adicionar", key=f"add_{produto['CODIGO']}"):
                quantidade = st.session_state.get(f"quantidade_{produto['CODIGO']}", 1)
                st.session_state['carrinho'].append({
                    "produto": produto['PRODUTO'],
                    "preco": produto['PRECO_VENDA'],
                    "quantidade": quantidade,
                    "id": produto['CODIGO']
                })
                mensagem_sucesso = f"{quantidade} unidade(s) de {produto['PRODUTO']} adicionada(s) ao carrinho."

            # Atualiza a mensagem de sucesso no card
            st.markdown(f"<script>document.getElementById('success_{index}').innerText = '{mensagem_sucesso}';</script>", unsafe_allow_html=True)

    # Botão de navegação para a próxima página
    if fim < len(produtos):
        if st.button("Próximos Produtos"):
            st.session_state['pagina'] += 1
            st.experimental_rerun()

    # Exibindo o carrinho
    if st.session_state['carrinho']:
        st.markdown("<h2>Carrinho</h2>", unsafe_allow_html=True)
        total = 0
        for item in st.session_state['carrinho']:
            subtotal = item['preco'] * item['quantidade']
            total += subtotal
            st.markdown(f"<div><p>{item['quantidade']}x {item['produto']} - R$ {subtotal:.2f}</p></div>", unsafe_allow_html=True)

        st.markdown(f"<h3>Total: R$ {total:.2f}</h3>", unsafe_allow_html=True)

if __name__ == "__main__":
    loja_virtual()
