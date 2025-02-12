import streamlit as st

# Função para remover traços
def remover_tracos(texto):
    return texto.replace("-", "/")  # Remove todos os traços

# Campos de entrada
campo_data = st.date_input("Data de Abertura Vaga")
campo_data = campo_data.strftime("%d/%m/%Y")
descricao = st.text_input("Descrição da Vaga:", "")
descricao = remover_tracos(descricao)  # Remove traços da descrição

# Menus suspensos (selectbox)
campo_menu_1 = st.selectbox("Localização da Vaga:", ["ITANHANDU/MG", "PRIMAVERA DO LESTE/MT", "LORENA/SP", "FORMOSA/GO", "FRANCISCO BELTRÃO/PR", "CANELA/SC", "DESCALVADO/SP", "CAMPANHA/MG", "PASSA QUATRO/MG", "UBERLÂNDIA/MG", "CÉU AZUL/PR", "ÁGUA BOA/MT", "CONFRESA/MT", "RIZOMA", "FAZENDA DA TOCA"])
campo_menu_2 = st.text_input("Setor:")
campo_menu_2 = remover_tracos(campo_menu_2)  # Remove traços do setor

campo_menu_3 = st.text_input("Turno:")
campo_menu_3 = remover_tracos(campo_menu_3)  # Remove traços do turno


# Botão para gerar a concatenação
if st.button("Gerar Concatenação"):
    # Concatenação dos dados separados por traço
    concatenacao = f"{campo_data} - {descricao} - {campo_menu_1} - {campo_menu_2} - {campo_menu_3}"
    
    # Exibir a concatenação
    st.write("Resultado da concatenação:")
    st.code(concatenacao)

    
