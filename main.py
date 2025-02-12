import streamlit as st
# Título do site
st.title("Gerador de Concatenação de Dados")

# Campos de entrada
campo_data = st.date_input("Selecione uma data")
campo_data = campo_data.strftime("%d/%m/%Y")
campo_digitavel = st.text_input("Digite algo", "")

# Menus suspensos (selectbox)
campo_menu_1 = st.selectbox("Escolha uma opção no primeiro menu", ["Opção 1", "Opção 2", "Opção 3"])
campo_menu_2 = st.selectbox("Escolha uma opção no segundo menu", ["A", "B", "C"])

# Botão para gerar a concatenação
if st.button("Gerar Concatenação"):
    # Concatenação dos dados separados por traço
    concatenacao = f"{campo_data} - {campo_digitavel} - {campo_menu_1} - {campo_menu_2}"
    
    # Exibir a concatenação
    st.write("Resultado da concatenação:")
    st.code(concatenacao)
    
    
