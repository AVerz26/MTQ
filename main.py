import streamlit as st

# Função para remover traços
def remover_tracos(texto):
    return texto.replace("-", "/")  # Substitui traços por barras

# Cabeçalho
st.header("Geração de texto - VAGAS INTERNAS")
st.write("")

# Campos de entrada
col1, col2, col3 = st.columns(3)

with col1:
    campo_data = st.date_input("Data de Abertura Vaga")
    campo_data = campo_data.strftime("%d/%m/%Y")

with col2:
    descricao = st.text_input("Descrição da Vaga:", "")

# Menus suspensos (selectbox)
with col3:
    campo_menu_1 = st.selectbox("Localização da Vaga:", ["ITANHANDU/MG", "PRIMAVERA DO LESTE/MT", "LORENA/SP", "FORMOSA/GO", "FRANCISCO BELTRÃO/PR", "CANELA/SC", "DESCALVADO/SP", "CAMPANHA/MG", "PASSA QUATRO/MG", "UBERLÂNDIA/MG", "CÉU AZUL/PR", "ÁGUA BOA/MT", "CONFRESA/MT", "RIZOMA", "FAZENDA DA TOCA"])

# Colunas para Setor e Turno
coli1, coli2, coli3 = st.columns(3)

with coli1:
    campo_menu_2 = st.text_input("Setor:")

with coli2:
    campo_menu_3 = st.text_input("Turno e descrição adicionais:")

# Remover traços
descricao = remover_tracos(descricao)  # Remove traços da descrição
campo_menu_2 = remover_tracos(campo_menu_2)  # Remove traços do setor
campo_menu_3 = remover_tracos(campo_menu_3)  # Remove traços do turno

# Verificar se todos os campos estão preenchidos
if st.button("Gerar Concatenação"):
    if not campo_data or not descricao or not campo_menu_1 or not campo_menu_2 or not campo_menu_3:
        st.error("Por favor, preencha todos os campos obrigatórios!")
    else:
        # Concatenação dos dados separados por traço
        concatenacao = f"{campo_data} - {descricao} - {campo_menu_1} - {campo_menu_2} - {campo_menu_3}"
        
        # Exibir a concatenação
        st.write("")
        st.write("Resultado:")
        st.code(concatenacao)
