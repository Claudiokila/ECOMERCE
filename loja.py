import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageOps
from crud import adicionar_produto, carregar_produtos, atualizar_produto, deletar_produto

st.set_page_config(layout="wide")


def redimensionar_imagem(caminho_imagem, largura_padrao=400, altura_padrao=400):
    imagem = Image.open(caminho_imagem)
    return imagem.resize((largura_padrao, altura_padrao))

def bordas_arredondadas(imagem, porcentagem_raio=25):
    largura, altura = imagem.size
    raio = int(min(largura, altura) * porcentagem_raio / 100)
    mask = Image.new('L', (largura, altura), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (largura, altura)], radius=raio, fill=255)
    imagem_arredondada = ImageOps.fit(imagem, (largura, altura))
    imagem_arredondada.putalpha(mask)
    return imagem_arredondada

def loja_virtual():
    st.markdown("""<style>
        .main { background-color: #1A3680; }
        header { background-color: #E50320; padding: 15px; border-radius: 10px; }
        h1 { color: white; text-align: center; font-size: 3em; }
        .item-carrinho { background-color: #789899; color: white; padding: 15px; margin-bottom: 10px; }
    </style>""", unsafe_allow_html=True)

    st.markdown("<header><h1>FARMÁCIA LÁ DE CASA</h1></header>", unsafe_allow_html=True)

    produtos = carregar_produtos()

    filtro = st.text_input("Buscar produto", key="filtro")
    if filtro:
        produtos = produtos[produtos['PRODUTO'].str.contains(filtro, case=False)]

    if 'carrinho' not in st.session_state:
        st.session_state['carrinho'] = []
    
    if 'pagina' not in st.session_state:
        st.session_state['pagina'] = 0
    
    produtos_por_pagina = 10  # Defina quantos produtos você quer mostrar por página
    total_paginas = (len(produtos) + produtos_por_pagina - 1) // produtos_por_pagina

    

    # Exibição dos produtos da página atual
    inicio = st.session_state['pagina'] * produtos_por_pagina
    fim = min(inicio + produtos_por_pagina, len(produtos))
    produtos_a_exibir = produtos.iloc[inicio:fim]

    def adicionar_ao_carrinho(produto, quantidade):
        item_carrinho = {
            "produto": produto['PRODUTO'],
            "preco": produto['PRECO_VENDA'],
            "quantidade": quantidade,
            "id": produto['CODIGO']
        }
        st.session_state['carrinho'].append(item_carrinho)

    for index, produto in produtos_a_exibir.iterrows():
        col1, col2 = st.columns([1, 2])
        with col1:
            caminho_imagem = f"imagens/salveo.jpg" # Atualize conforme necessário
            imagem_redimensionada = redimensionar_imagem(caminho_imagem)
            imagem_com_bordas = bordas_arredondadas(imagem_redimensionada)
            st.image(imagem_com_bordas)

        with col2:
            st.markdown(f"<h3>{produto['PRODUTO']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p>Preço: R$ {produto['PRECO_VENDA']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>Descrição: {produto['PRODUTO']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>Quantidade disponível: {produto['ESTOQUE']}</p>", unsafe_allow_html=True)

            with st.form(key=f"form_{produto['CODIGO']}"):
                col_qtd, col_btn = st.columns([1, 2])
                with col_qtd:
                    quantidade = st.number_input("Quantidade", min_value=1, max_value=produto['ESTOQUE'], step=1, label_visibility="collapsed")
                with col_btn:
                    if st.form_submit_button(f"Adicionar {produto['PRODUTO']} ao carrinho"):
                        adicionar_ao_carrinho(produto, quantidade)
                        st.success(f"{quantidade} unidade(s) de {produto['PRODUTO']} adicionada(s) ao carrinho.")

    # Navegação entre páginas
    if st.button("Página Anterior") and st.session_state['pagina'] > 0:
        st.session_state['pagina'] -= 1
    st.write(f"Página {st.session_state['pagina'] + 1} de {total_paginas}")
    if st.button("Próxima Página") and st.session_state['pagina'] < total_paginas - 1:
        st.session_state['pagina'] += 1


    if st.session_state['carrinho']:
        st.markdown("<h2>Carrinho</h2>", unsafe_allow_html=True)
        total = 0
        for item in st.session_state['carrinho']:
            subtotal = item['preco'] * item['quantidade']
            total += subtotal
            st.markdown(f"<div class='item-carrinho'><p>{item['quantidade']}x {item['produto']} - R$ {subtotal:.2f}</p></div>", unsafe_allow_html=True)

        st.markdown(f"<h3>Total: R$ {total:.2f}</h3>", unsafe_allow_html=True)

if __name__ == "__main__":
    loja_virtual()
