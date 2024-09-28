import pandas as pd
import streamlit as st
import requests

# CSS para aplicar o background azul claro e cor nos botões
st.markdown(
    f"""
    <style>
    .main {{
        background-color: #E0F7FA;  /* Cor de fundo azul bebê para o corpo principal */
    }}
    header {{
        background-color: #1565C0;  /* Cor de fundo azul para o cabeçalho */
        padding: 10px;
    }}
    h1 {{
        color: white;  /* Cor do texto do título principal */
        text-align: center; /* Centraliza o texto */
    }}
    h2, h3, p {{
        color: #0D47A1;  /* Cor do texto nas outras seções */
    }}
    .stButton > button {{
        background-color: #1565C0; /* Cor azul para os botões */
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px;
    }}
    .stButton > button:hover {{
        background-color: #0D47A1; /* Cor ao passar o mouse nos botões */
    }}
    .item-carrinho {{
        background-color: #BBDEFB; /* Cor de fundo azul claro para itens do carrinho */
        color: #0D47A1;  /* Cor do texto */
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
    }}
    .item-carrinho:hover {{
        background-color: #64B5F6; /* Cor de fundo ao passar o mouse no item do carrinho */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Função para gerar o link de redirecionamento para Instagram
def redirecionar_para_instagram(dados_compra):
    mensagem = f"Compra finalizada! Detalhes: {dados_compra}"
    mensagem_codificada = requests.utils.quote(mensagem)
    url_instagram = f"https://www.instagram.com/direct/new/?text={mensagem_codificada}&username=farmacialadecasa_"
    return url_instagram

# Função para visualizar o carrinho
def visualizar_carrinho():
    if 'carrinho' not in st.session_state:
        st.session_state['carrinho'] = []

    if st.session_state['carrinho']:
        st.markdown("<header><h1>FARMÁCIA LÁ DE CASA</h1></header>", unsafe_allow_html=True)
        st.markdown("<h2>Carrinho</h2>", unsafe_allow_html=True)
        total = 0

        for item in st.session_state['carrinho']:
            # Corrigir o formato do preço antes de converter para float
            preco = float(item['preco'].replace(",", "."))
            subtotal = preco * item['quantidade']
            total += subtotal
            st.markdown(
                f"""
                <div class="item-carrinho">
                    <p>{item['quantidade']}x {item['produto']} - R$ {subtotal:.2f}</p>
                    <p>Preço unitário: R$ {preco:.2f}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(f"Remover {item['produto']} do carrinho", key=f"remover_{item['id']}"):
                st.session_state['carrinho'] = [i for i in st.session_state['carrinho'] if i['id'] != item['id']]
                st.success("Item removido do carrinho.")

        st.markdown(f"<h3>Total: R$ {total:.2f}</h3>", unsafe_allow_html=True)

        st.subheader("Forma de Entrega")
        entrega = st.radio("Escolha a forma de entrega:", ("Retirar na loja", "Solicitar entrega"))

        if entrega == "Solicitar entrega":
            taxa_entrega = 5.00
            total += taxa_entrega
            st.markdown(f"<h4>Taxa de entrega: R$ {taxa_entrega:.2f}</h4>", unsafe_allow_html=True)

            nome_usuario = st.text_input("Nome do Usuário", "")
            rua = st.text_input("Rua", "")
            numero = st.number_input("Número da Rua", min_value=1, value=1)
            complemento = st.text_input("Complemento", "")
            cep = st.text_input("CEP (8 dígitos)", "", max_chars=8)
            telefone = st.text_input("Telefone (com DDD)", "")

            pagamento = st.selectbox("Forma de pagamento", ["Pix", "Cartão", "Dinheiro na entrega"])

            st.subheader("Resumo da Compra")
            st.write(f"Forma de Entrega: {entrega}")
            st.write(f"Nome do Usuário: {nome_usuario}")
            st.write(f"Endereço: {rua}, {numero}, {complemento}, CEP: {cep}")
            st.write(f"Telefone: {telefone}")
            st.write(f"Forma de Pagamento: {pagamento}")
            st.write(f"Total Final: R$ {total:.2f}")

            if st.button("Finalizar compra"):
                if not nome_usuario or not rua or not cep or not telefone:
                    st.warning("Por favor, preencha todos os campos obrigatórios.")
                elif len(cep) != 8:
                    st.warning("O CEP deve ter 8 dígitos.")
                else:
                    dados_compra = {
                        "nome_usuario": nome_usuario,
                        "endereco": {"rua": rua, "numero": numero, "complemento": complemento, "cep": cep},
                        "telefone": telefone,
                        "entrega": entrega,
                        "pagamento": pagamento,
                        "total": total,
                        "itens": st.session_state['carrinho']
                    }

                    link_instagram = redirecionar_para_instagram(dados_compra)
                    st.markdown(f"[Clique aqui para finalizar sua compra e enviar uma mensagem no Instagram]({link_instagram})", unsafe_allow_html=True)

                    st.session_state['carrinho'] = []
                    st.success("Compra finalizada com sucesso! Seu carrinho foi esvaziado.")

        else:
            st.write("Você escolheu retirar na loja.")
            pagamento = st.selectbox("Forma de pagamento", ["Pix", "Cartão", "Dinheiro na entrega"])
            st.write(f"Forma de Pagamento: {pagamento}")
            st.write(f"Total Final: R$ {total:.2f}")

            if st.button("Finalizar compra"):
                dados_compra = {
                    "nome_usuario": "Cliente Retirada na Loja",
                    "endereco": {"rua": "Retirada na loja", "numero": "", "complemento": "", "cep": ""},
                    "telefone": "",
                    "entrega": entrega,
                    "pagamento": pagamento,
                    "total": total,
                    "itens": st.session_state['carrinho']
                }

                link_instagram = redirecionar_para_instagram(dados_compra)
                st.markdown(f"[Clique aqui para finalizar sua compra e enviar uma mensagem no Instagram]({link_instagram})", unsafe_allow_html=True)

                st.session_state['carrinho'] = []
                st.success("Compra finalizada com sucesso! Seu carrinho foi esvaziado.")

    else:
        st.warning("Seu carrinho está vazio. Adicione produtos antes de visualizar.")

if __name__ == "__main__":
    visualizar_carrinho()
