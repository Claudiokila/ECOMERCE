import pandas as pd
import streamlit as st

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

# Função para visualizar o carrinho
def visualizar_carrinho():
    if 'carrinho' not in st.session_state:
        st.session_state['carrinho'] = []

    # Exibir carrinho
    if st.session_state['carrinho']:
        st.markdown("<header><h1>FARMÁCIA LÁ DE CASA</h1></header>", unsafe_allow_html=True)
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
                st.session_state['carrinho'] = [i for i in st.session_state['carrinho'] if i['id'] != item['id']]
                st.success("Item removido do carrinho.")

        st.markdown(f"<h3>Total: R$ {total:.2f}</h3>", unsafe_allow_html=True)

        # Opções de entrega
        st.subheader("Forma de Entrega")
        entrega = st.radio("Escolha a forma de entrega:", ("Retirar na loja", "Solicitar entrega"))

        # Se a entrega for solicitada, adicionar taxa
        if entrega == "Solicitar entrega":
            taxa_entrega = 5.00
            total += taxa_entrega
            st.markdown(f"<h4>Taxa de entrega: R$ {taxa_entrega:.2f}</h4>", unsafe_allow_html=True)

            # Campos obrigatórios para o endereço
            nome_usuario = st.text_input("Nome do Usuário", "")
            rua = st.text_input("Rua", "")
            numero = st.number_input("Número da Rua", min_value=1, value=1)
            complemento = st.text_input("Complemento", "")
            cep = st.text_input("CEP (8 dígitos)", "", max_chars=8)
            telefone = st.text_input("Telefone (com DDD)", "")

            # Escolher forma de pagamento
            pagamento = st.selectbox("Forma de pagamento", ["Pix", "Cartão", "Dinheiro na entrega"])

            # Exibir resumo final
            st.subheader("Resumo da Compra")
            st.write(f"Forma de Entrega: {entrega}")
            st.write(f"Nome do Usuário: {nome_usuario}")
            st.write(f"Endereço: {rua}, {numero}, {complemento}, CEP: {cep}")
            st.write(f"Telefone: {telefone}")
            st.write(f"Forma de Pagamento: {pagamento}")
            st.write(f"Total Final: R$ {total:.2f}")

            # Botão para finalizar a compra
            if st.button("Finalizar compra"):
                if not nome_usuario or not rua or not cep or not telefone:
                    st.warning("Por favor, preencha todos os campos obrigatórios.")
                elif len(cep) != 8:
                    st.warning("O CEP deve ter 8 dígitos.")
                else:
                    st.session_state['carrinho'] = []
                    st.success("Compra finalizada com sucesso! Seu carrinho foi esvaziado.")

        else:  # Retirar na loja
            st.write("Você escolheu retirar na loja.")

            # Escolher forma de pagamento
            pagamento = st.selectbox("Forma de pagamento", ["Pix", "Cartão", "Dinheiro na entrega"])

            st.write(f"Forma de Pagamento: {pagamento}")
            st.write(f"Total Final: R$ {total:.2f}")

            # Botão para finalizar a compra
            if st.button("Finalizar compra"):
                st.session_state['carrinho'] = []
                st.success("Compra finalizada com sucesso! Seu carrinho foi esvaziado.")

    else:
        st.warning("Seu carrinho está vazio. Adicione produtos antes de visualizar.")

if __name__ == "__main__":
    visualizar_carrinho()
