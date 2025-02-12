import streamlit as st
# Campos de entrada
campo_data = st.date_input("Data de Abertura Vaga")
campo_data = campo_data.strftime("%d/%m/%Y")
descricao = st.text_input("Descrição da Vaga:", "")

# Menus suspensos (selectbox)
campo_menu_1 = st.selectbox("Localização da Vaga:", ["Opção 1", "Opção 2", "Opção 3"])
campo_menu_2 = st.selectbox("Setor:", ["A", "B", "C"])

campo_menu_3 = st.text_input("Turno:")

# Botão para gerar a concatenação
if st.button("Gerar Concatenação"):
    # Concatenação dos dados separados por traço
    concatenacao = f"{campo_data} - {campo_digitavel} - {campo_menu_1} - {campo_menu_2} - {campo_menu_3}"
    
    # Exibir a concatenação
    st.write("Resultado da concatenação:")
    st.code(concatenacao)
    
    
