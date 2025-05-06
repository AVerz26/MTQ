import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config("MTQ VAGAS", layout = "wide")
# Função para remover traços
def remover_tracos(texto):
    return texto.replace("-", ":")  # Substitui traços por barras

# Cabeçalho
st.header("Gerador de texto - VAGAS INTERNAS")
st.write("")

# Campos de entrada
col1, col2, col3 = st.columns(3)

with col1:
    campo_data = st.date_input("Data de Abertura da Vaga")
    campo_data = campo_data.strftime("%d/%m/%Y")

with col2:
    descricao = st.text_input("Descrição da Vaga:", "")

# Menus suspensos (selectbox)
with col3:
    campo_menu_1 = st.selectbox("Localização da Vaga:", ["ITANHANDU/MG", "PRIMAVERA DO LESTE/MT", "LORENA/SP", "FORMOSA/GO", "FRANCISCO BELTRÃO/PR", "CANELA/SC", "DESCALVADO/SP", "CAMPANHA/MG", "PASSA QUATRO/MG", "UBERLÂNDIA/MG", "CÉU AZUL/PR", "ÁGUA BOA/MT", "CONFRESA/MT", "RIZOMA", "FAZENDA DA TOCA"])

# Colunas para Setor e Turno
coli1, coli2, coli3 = st.columns(3)
setores = [
    "ADM/SUPORTE", "AGRICULTURA", "ALMOXARIFADO", "ARMAZÉM", 
    "CLASSIFICAÇÃO DE OVOS", "COMERCIAL", "CONTROLE DE QUALIDADE", "DEPÓSITO DE EMBALAGEM", 
    "EXPEDIÇÃO DE OVOS", "EXPEDIÇÃO DE RAÇÃO", "FÁBRICA DE RAÇÃO", 
    "HIGIENIZAÇÃO OPERACIONAL", "HIGIENIZAÇÃO PRÉ-OPERACIONAL", "LAVANDERIA",
    "MANUTENÇÃO", "ORIGINAÇÃO", "PASTEURIZAÇÃO DE OVOS", 
    "PÁ CARREGADEIRA", "PCP", "POSTURA", "RECEBIMENTO", "RECRIA", 
    "SERVIÇOS GERAIS", "SSMA", "TRANSPORTE ESTERCO", "TRATOR", "USINA DE COMPOSTAGEM"
]

with coli1:
    campo_menu_2 = st.selectbox("Setor:", setores)

with coli2:
    campo_menu_3 = st.text_input("Turno e descrição adicional:")
with coli3:
    resp = st.text_input("Responsável pela abertura da vaga:")

# Remover traços
descricao = remover_tracos(descricao)  # Remove traços da descrição
campo_menu_2 = remover_tracos(campo_menu_2)  # Remove traços do setor
campo_menu_3 = remover_tracos(campo_menu_3)  # Remove traços do turno

# Verificar se todos os campos estão preenchidos
if st.button("Gerar Resultado"):
    if not campo_data or not descricao or not campo_menu_1 or not campo_menu_2 or not campo_menu_3:
        st.error("Por favor, preencha todos os campos obrigatórios!")
    else:
        # Concatenação dos dados separados por traço
        concatenacao = f"{campo_data} - {descricao} - {campo_menu_1} - {campo_menu_2} - {campo_menu_3}"
        
        # Exibir a concatenação
        st.write("")
        st.write("Resultado:")
        st.code(concatenacao)
        st.warning("Manter a formatação correta desse texto para o Forms, pois se usar o '-' desconfigurará o dashboard!")

    df = pd.DataFrame([
        {
            "Data":campo_data,
            "Descrição Vaga":descricao,
            "Localização da Vaga": campo_menu_1,
            "Setor": campo_menu_2,
            "Descrição Adicional": campo_menu_3,
            "Responsável": resp
        }
    ])
        

    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        st.write("ok")
        existing_data = conn.read(worksheet="principal", usecols=[0, 1, 2, 3, 4, 5],  ttl=10)
        st.write("ok")
        existing_data = existing_data.dropna(how="all")
        st.write("ok")
        update_df = pd.concat([existing_data, df], ignore_index=True)      
        st.write("ok")
        conn.update(worksheet="principal", data=update_df)  
        st.write("ok")
    except:
        st.write("o")
