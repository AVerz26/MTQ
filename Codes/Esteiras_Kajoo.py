import streamlit as st
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import matplotlib.pyplot as plat
import matplotlib.pyplot as plty
import matplotlib.pyplot as pltyu
from datetime import datetime, timedelta
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import StringIO
import seaborn as sns
import altair as alt
import plotly.express as px
import warnings
import math
import mysql.connector

st.set_page_config(
    page_title="ANÁLISE KAJOO",
    page_icon="🥚",
)

warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)

def calcular_variacao(coluna, hi, hf):
    # Filtrar os valores entre 'hi' e 'hf'
    valores = coluna[(linhas_dados['Hora'] >= hi) & (linhas_dados['Hora'] <= hf)]
    # Verificar se há valores suficientes para calcular a variação
    if len(valores) >= 2:
        # Calcular a diferença entre o último e o primeiro valor
        variacao = int((valores.iloc[-1] - valores.iloc[0]) / 360)
    else:
        # Se não houver valores suficientes, definir a variação como 0
        variacao = 0
    return variacao

# Obter a data atual
data_atual = pd.Timestamp.now().date()

# Carregar os dados
dados = pd.read_csv('Combinado_BI.csv', parse_dates=[0], dayfirst=True, delimiter=';')
status = pd.read_csv('StatusEST.csv', parse_dates=[0], dayfirst=True, delimiter=';', encoding='ISO-8859-1')


dados = dados[dados['Total'] != 0]

dados['G1'] = dados['Esteira 1'] - dados['Total E1']
dados['G7'] = dados['Esteira 7'] - dados['Total E7']
dados['G13'] = dados['Esteira 13'] - dados['Total E13']
dados['G19'] = dados['Esteira 19'] - dados['Total E19']
dados['G25'] = dados['Esteira 25'] - dados['Total E25']
dados['G31'] = dados['Esteira 31'] - dados['Total E31']
dados['G37'] = dados['Esteira 37'] - dados['Total E37']
dados['G46'] = dados['Esteira 46'] - dados['Total E46']

colunas_esteira = ['Esteira 1', 'Esteira 7', 'Esteira 13', 'Esteira 19', 'Esteira 25', 'Esteira 31', 'Esteira 37', 'Esteira 46']
colunas_total_e = ['Total E1', 'Total E7', 'Total E13', 'Total E19', 'Total E25', 'Total E31', 'Total E37', 'Total E46']

# Iterando sobre cada par de colunas Esteira e Total E
for esteira_col, total_e_col in zip(colunas_esteira, colunas_total_e):
    for index, row in dados.iterrows():
        if row[total_e_col] > row[esteira_col]:
            dados.at[index, esteira_col] = row[total_e_col]



# Reordenar as colunas para colocar "G13" na posição de "Total E13"
colunas = list(dados.columns)
colunas.insert(9, colunas.pop(colunas.index('G1')))
colunas.insert(16, colunas.pop(colunas.index('G7')))
colunas.insert(23, colunas.pop(colunas.index('G13')))
colunas.insert(30, colunas.pop(colunas.index('G19')))
colunas.insert(37, colunas.pop(colunas.index('G25')))
colunas.insert(44, colunas.pop(colunas.index('G31')))
colunas.insert(51, colunas.pop(colunas.index('G37')))
colunas.insert(61, colunas.pop(colunas.index('G46')))

dados = dados[colunas]

# Excluir a coluna "Total E13" dos dados
dados.drop(columns=['Total'], inplace=True)
dados.drop(columns=['Total E1'], inplace=True)
dados.drop(columns=['Total E7'], inplace=True)
dados.drop(columns=['Total E13'], inplace=True)
dados.drop(columns=['Total E19'], inplace=True)
dados.drop(columns=['Total E25'], inplace=True)
dados.drop(columns=['Total E31'], inplace=True)
dados.drop(columns=['Total E37'], inplace=True)
dados.drop(columns=['Total E46'], inplace=True)

# Definir a lista de datas disponíveis
datas_disponiveis = dados['Data'].dt.date.unique()



st.title(":egg: Rastreio das Esteiras de Ovos")

# Definir a lista de datas disponíveis
datas_disponiveis = dados['Data'].dt.date.unique()

# Exibir o seletor de data
data_selecionada = st.date_input("Selecione uma data:", min_value=min(datas_disponiveis), max_value=max(datas_disponiveis), value=max(datas_disponiveis))

# Ler o arquivo CSV
data_nasc = pd.read_excel('DATA_NASC.xlsx')


# Obter a data atual
data_atual = data_selecionada

# Calcular a diferença em semanas para cada coluna
diferencas_em_semanas = {}
for coluna, data_nascimento in data_nasc.items():
    # Verificar se a coluna contém datas
    if isinstance(data_nascimento[0], datetime):
        # Calcular a diferença em semanas
        diferenca_em_semanas = (pd.Timestamp(data_atual) - data_nascimento[0]).days / 7
        # Armazenar a diferença em semanas para a coluna atual
        diferencas_em_semanas[coluna] = int(diferenca_em_semanas)

for i, coluna in enumerate(dados.columns[1:], start=1):
    # Incrementar o nome da coluna com o valor correspondente de diferencas_em_semanas
    novo_nome_coluna = f"{coluna} - [{diferencas_em_semanas.get(coluna, 0)} s.]"
    dados = dados.rename(columns={coluna: novo_nome_coluna})


# Filtrar o DataFrame de acordo com a data selecionada
dados_filtrados = dados[dados['Data'].dt.date == data_selecionada]

# Remover duplicatas do DataFrame filtrado
dados_filtrados = dados_filtrados.drop_duplicates(subset=['Data'])

# Converter a primeira coluna para datetime apenas uma vez
dados_filtrados['Data'] = pd.to_datetime(dados_filtrados['Data'])

# Calcular o valor decimal para cada hora
dados_filtrados['Hora'] = dados_filtrados['Data'].dt.hour + dados_filtrados['Data'].dt.minute / 60


dados_desempenho = dados[['Data'] + list(dados.columns[1:9])]

#dados_desempenho['Soma'] = dados_desempenho.iloc[:, 1:9].sum(axis=1) / 360

# Usando .loc para definir o valor diretamente no DataFrame original
dados_desempenho.loc[:, 'Soma'] = dados_desempenho.iloc[:, 1:9].sum(axis=1) / 360

# Filtrar o DataFrame de acordo com a data selecionada
dados_desempenho_filtrados = dados_desempenho[dados_desempenho['Data'].dt.date == data_selecionada]

for i in range(1, len(dados_desempenho_filtrados)):
    # Comparando os valores da coluna "Total" entre linhas sucessivas
    if dados_desempenho_filtrados.iloc[i]['Soma'] < dados_desempenho_filtrados.iloc[i - 1]['Soma']:
        # Atualizando o valor na última linha da coluna "Total"
        dados_desempenho_filtrados.iloc[-1, dados_desempenho_filtrados.columns.get_loc('Soma')] += (
            dados_desempenho_filtrados.iloc[i - 1]['Soma'] - dados_desempenho_filtrados.iloc[i]['Soma']
        )

#st.dataframe(dados_desempenho_filtrados)
# Remover duplicatas do DataFrame filtrado
dados_desempenho_filtrados = dados_desempenho_filtrados.drop_duplicates(subset=['Data'])

# Converter a primeira coluna para datetime apenas uma vez
dados_desempenho_filtrados['Data'] = pd.to_datetime(dados_desempenho_filtrados['Data'])

# Calcular o valor decimal para cada hora
dados_desempenho_filtrados['Hora'] = dados_desempenho_filtrados['Data'].dt.hour + dados_desempenho_filtrados['Data'].dt.minute / 60

dados_filtrados1 = dados_filtrados.sort_values('Data', ascending=False)
ultima_hora = max(dados_filtrados['Hora'])

horas = int(ultima_hora)  # Extrai a parte inteira das horas
minutos = int((ultima_hora - horas) * 60)

hora_formatada = datetime(1900, 1, 1, horas, minutos)
hora_formatada_str = hora_formatada.strftime("%H:%M")


col1, col2 = st.columns(2)
with col1:
    st.markdown("<div style='text-align: right'><b>Contagem EP: {} caixas</b></div>".format(int(sum(max(dados_filtrados[column]) for column in dados_filtrados.columns[1:9])/360)), unsafe_allow_html=True)

# Centralize o conteúdo de col2
with col2:
    st.markdown("<div style='text-align: left'><small><em>(Última atualização: {} horas)</em></small></div>".format(hora_formatada_str), unsafe_allow_html=True)



# Agora você pode usá-lo no seu código

opcao_colunas = st.radio('Selecione uma opção:', ['Esteiras principais', 'Todos os Galpões', 'POSTURA N1', 'POSTURA N2'], horizontal = True)
opfinal = opcao_colunas
# Criar as abas
tabs = st.tabs([":bar_chart: Gráfico", ":mag: Percentual Ovos por Hora", ":chart_with_upwards_trend: Performance Hora-Hora",":large_green_circle: Status Contador", "🐣 Ovos Fissurados"])



# Gráfico
with tabs[0]:
    # Filtrar o DataFrame de acordo com a data selecionada
    dados_filtrados_grafico = dados[dados['Data'].dt.date == data_selecionada]

    # Remover duplicatas do DataFrame filtrado
    dados_filtrados_grafico = dados_filtrados_grafico.drop_duplicates(subset=['Data'])

    colunas_exibir = []  # Definir uma lista vazia inicialmente

    if opcao_colunas == 'Esteiras principais':
        colunas_exibir = dados.columns[1:9]  # Colunas da 2ª à 9ª
        ctm = 3000
    elif opcao_colunas == 'Todos os Galpões':
        colunas_exibir = dados.columns[9:]
        ctm = 1080
    elif opcao_colunas == 'POSTURA N1':
        colunas_exibir = dados.columns[9:33]  # Colunas da 10ª à 36ª
        ctm = 1080
    elif opcao_colunas == 'POSTURA N2':
        colunas_exibir = dados.columns[33:]  # Colunas da 37ª até a última
        ctm = 1080


    # Filtrar os dados pelas colunas a serem exibidas
    dados_filtrados_grafico = dados_filtrados_grafico[['Data'] + list(colunas_exibir)]

    # Converter a primeira coluna para datetime apenas uma vez
    dados_filtrados_grafico['Data'] = pd.to_datetime(dados_filtrados_grafico['Data'])

    # Calcular o valor decimal para cada hora
    dados_filtrados_grafico['Hora'] = dados_filtrados_grafico['Data'].dt.hour + dados_filtrados_grafico['Data'].dt.minute / 60
    hora_inicio = st.slider('Hora de Início', min_value=int(dados_filtrados_grafico['Hora'].min()), max_value=int(dados_filtrados_grafico['Hora'].max()), value=int(dados_filtrados_grafico['Hora'].min()))
    hora_fim = st.slider('Hora de Fim', min_value=hora_inicio+1, max_value=int(dados_filtrados_grafico['Hora'].max())+1, value=int(dados_filtrados_grafico['Hora'].max()))

    # Filtrar os dados com base nos horários selecionados
    dados_filtrados_grafico = dados_filtrados_grafico[(dados_filtrados_grafico['Hora'] >= hora_inicio) & (dados_filtrados_grafico['Hora'] <= hora_fim)]

# Inicializar o dicionário de intervalos por esteira
    intervalos_por_esteira = {}

# Encontrar os intervalos de tempo em que cada esteira está ativa
    for esteira in colunas_exibir[0:]:
        intervalos = []
        inicio = None
        for i in range(len(dados_filtrados_grafico) - 1):
            diferenca = dados_filtrados_grafico[esteira].iloc[i + 1] - dados_filtrados_grafico[esteira].iloc[i]
            if diferenca > ctm:
                if inicio is None:
                    inicio = dados_filtrados_grafico['Hora'].iloc[i]
            elif inicio is not None:
                intervalos.append((inicio, dados_filtrados_grafico['Hora'].iloc[i]))
                inicio = None
        if inicio is not None:
            intervalos.append((inicio, dados_filtrados_grafico['Hora'].iloc[-1]))
        intervalos_por_esteira[esteira] = intervalos

# Criar o gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 8))

    for i, (esteira, intervalos) in enumerate(intervalos_por_esteira.items()):
            for intervalo in intervalos:
                ax.barh(esteira, intervalo[1] - intervalo[0], left=intervalo[0], height=0.3, color='#061b96')  


    # Configurações do gráfico
    ax.set_xlabel('Hora')
    ax.set_ylabel('Esteiras')

    # Encontrar a data mais recente no DataFrame filtrado
    data_mais_recente = dados_filtrados_grafico['Data'].max()

    # Encontrar a hora do último valor para a data mais recente
    hora_ultimo_valor = dados_filtrados_grafico[dados_filtrados_grafico['Data'] == data_mais_recente]['Hora'].iloc[-1]

    # Adicionar uma linha vertical vermelha no gráfico na hora do último valor
    ax.axvline(hora_ultimo_valor, color='#F76040', linestyle='--', label='Último valor para a data mais recente')
    data_selecionadinha = data_selecionada.strftime("%d/%m/%Y")
    # Título do gráfico
    ax.set_title('Horário de funcionamento das esteiras de ovos ({}) - {}'.format(data_selecionadinha, opcao_colunas))

    # Definir os intervalos e as marcações verticais no eixo x
    ax.set_xticks(range(25))
    ax.set_xticks(range(25), minor=True)
    ax.grid(which='both', axis='x', linestyle='--', linewidth=0.5, color='gray')

    # Definir o intervalo do eixo x
    ax.set_xlim(3, 24)
    fig.patch.set_edgecolor('black')  # Definir a cor da borda da figura como preto
    fig.patch.set_linewidth(5)        # Definir a largura da borda da figura

    # Exibir o gráfico
    st.pyplot(fig)

    st.write("🟦 - Tempo de duração de esteira/galpão ligado")

    plt.close(fig)


with tabs[1]:
    # Adicionar controles deslizantes para selecionar a hora de início e de fim
    hora_inicio_temp = st.slider('Hora de Início', min_value=int(dados_filtrados['Hora'].min()), max_value=int(dados_filtrados['Hora'].max()), value=int(dados_filtrados['Hora'].min()), key='hora_inicio_temp')
    hora_fim_temp = st.slider('Hora de Fim', min_value=hora_inicio_temp + 1, max_value=int(dados_filtrados['Hora'].max())+1, value=int(dados_filtrados['Hora'].max()), key='hora_fim_temp')

    colunas_exibir_temp = []  # Lista vazia inicialmente

    if opcao_colunas == 'Esteiras principais':
        colunas_exibir_temp = dados.columns[1:9].intersection(dados_filtrados.columns)  # Colunas da 2ª à 9ª
    elif opcao_colunas == 'POSTURA N1':
        colunas_exibir_temp = dados.columns[9:33].intersection(dados_filtrados.columns)  # Colunas da 10ª à 36ª
    elif opcao_colunas == 'POSTURA N2':
        colunas_exibir_temp = dados.columns[33:].intersection(dados_filtrados.columns)  # Colunas da 10ª à 36ª
    elif opcao_colunas == 'Todos os Galpões':
        colunas_exibir_temp = dados.columns[9:].intersection(dados_filtrados.columns)

    # Definir o índice do DataFrame como as esteiras correspondentes
    dados_filtrados.set_index('Data', inplace=True)
    
    # Calcular a variação para cada coluna de dados usando as horas selecionadas
    variacao_por_coluna = dados_filtrados[colunas_exibir_temp].apply(lambda x: max(0, int((x[(dados_filtrados['Hora'] >= hora_inicio_temp) & (dados_filtrados['Hora'] <= hora_fim_temp)].iloc[-1] - x[(dados_filtrados['Hora'] >= hora_inicio_temp) & (dados_filtrados['Hora'] <= hora_fim_temp)].iloc[0]) / 360)))

    # Calcular o total da variação para todas as colunas
    total_variacao = variacao_por_coluna.sum()

    # Calcular a porcentagem de cada valor em relação ao total
    porcentagem_por_coluna = variacao_por_coluna / total_variacao * 100
    porcentagem_por_coluna = round(porcentagem_por_coluna, 1)
    tabela_variacao_porcentagem = []
    # Criar um DataFrame com os valores da variação e porcentagem para cada esteira
    tabela_variacao_porcentagem = pd.DataFrame({
        'Caixas Colhidas': variacao_por_coluna,
        '% participação no total': porcentagem_por_coluna
    }, index=colunas_exibir_temp)  # Definir o índice como o nome das esteiras

    indices_destacados = ['G1', 'G7', 'G13', 'G19', 'G25', 'G31', 'G37', 'G46']

    # Função para pintar os índices
    def pintar_indices(valor):
        # Verificar se o valor é uma string e começa com 'G'
        if isinstance(valor, str) and valor.startswith('G') and valor in indices_destacados:
            return 'background-color: yellow'
        else:
            return ''
    
    # Função para formatar a porcentagem com uma casa decimal
    def formatar_porcentagem(valor):
        return f'{valor:.1f}'
    
    # Construir o DataFrame
    tabela_variacao_porcentagem = pd.DataFrame({
        'Caixas Colhidas': variacao_por_coluna,
        '% participação no total': porcentagem_por_coluna
    }, index=colunas_exibir_temp)  # Definir o índice como o nome das esteiras
    
    # Classificar o DataFrame pela coluna '% participação no total' em ordem decrescente
    tabela_variacao_porcentagem = tabela_variacao_porcentagem.sort_values(by='% participação no total', ascending=False)
    

# Exibir a tabela no Streamlit
    

    
    x = tabela_variacao_porcentagem.index.to_series().str.extract(r'\[(\d+)').astype(int)
    x = pd.concat([x, tabela_variacao_porcentagem], axis = 1)
    
    produto = x.iloc[:, 0] * x.iloc[:, 2]

    # Calcula a soma dos valores da terceira coluna
    soma_terceira_coluna = x.iloc[:, 2].sum()
    
    # Calcula a média ponderada
    media_ponderada = produto.sum() / soma_terceira_coluna

    st.markdown(f"<h5 style='text-align: center;'>Idade Ponderada: {int(media_ponderada)} semanas</h5>", unsafe_allow_html=True)


    st.table(tabela_variacao_porcentagem)


with tabs[2]:
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plotar a área em função da hora
    ax.fill_between(dados_desempenho_filtrados['Hora'], dados_desempenho_filtrados['Soma'], color='skyblue', alpha=0.4)
    hora = dados_desempenho_filtrados['Hora'].to_numpy()
    soma = dados_desempenho_filtrados['Soma'].to_numpy()

    ax.plot(hora, soma, 'o-')
    # Adicionar marcadores "o" aos pontos
   # ax.plot(dados_desempenho_filtrados['Hora'], dados_desempenho_filtrados['Soma'], color='blue', marker='o')
    
    # Calcular a diferença entre os valores de "Soma"
    diff_soma = np.diff(dados_desempenho_filtrados['Soma'])
    
    # Calcular a diferença entre as horas
    diff_horas = np.diff(dados_desempenho_filtrados['Hora'])
    
    # Calcular a derivada
    derivada = diff_soma / diff_horas
    
    # Configurações do gráfico
    data_selecionadinha = data_selecionada.strftime("%d/%m/%Y")
    ax.set_title('Desempenho das esteiras de ovos ({})'.format(data_selecionadinha))
    ax.set_xlabel('Hora')
    ax.set_ylabel('Produção Acumulada (cxs.)')
    ax.grid(True, alpha=0.4)
    
    # Adiciona um segundo eixo y para a derivada
    ax2 = ax.twinx()
    ax2.set_ylabel('Performance Esteiras (cxs./h)')
    hora = dados_desempenho_filtrados['Hora'].to_numpy()
     # Plotar a derivada no eixo secundário
    ax2.plot(hora[1:], derivada, color='red', marker='x')
    #ax2.plot(dados_desempenho_filtrados['Hora'][1:], derivada, color='red', marker='x')  # Plotar a partir do segundo ponto
    ax2.set_ylim(0, 1500)  # Define o intervalo do eixo y secundário
    ax2.axhline(y=500, color='green', linestyle='--', linewidth=1)
    ax2.axhline(y=1000, color='green', linestyle='--', linewidth=1)
    valores_inteiros = np.arange(int(min(dados_desempenho_filtrados['Hora'])), int(max(dados_desempenho_filtrados['Hora'])) + 1)

# Definir os marcadores dos ticks do eixo x para exibir apenas valores inteiros
    ax.set_xticks(valores_inteiros)
    
    fig.patch.set_edgecolor('black')  # Definir a cor da borda da figura como preto
    fig.patch.set_linewidth(5)        # Definir a largura da borda da figura

    # Exibir o gráfico
    st.pyplot(fig)

    
    st.write("🔵 - Produção Acumulada (cxs.)     ❌ - Performance Esteiras (cxs./h)")
    
    plt.close(fig)

    connection = mysql.connector.connect(host="127.0.0.1", user="mantiqueira", password="mantiqueira", database="MOBA")
    query = """
SELECT 
    DATE_FORMAT(DATE_ADD(Timestamp, INTERVAL 0 HOUR), '%Y/%m/%d %H:%00') AS hour,
    AVG(VarTotal) AS Prod_MOBA
FROM MOBA.DISP
GROUP BY hour;

"""
    query2 = """
SELECT *, 1 AS maquina
FROM MOBA.moba_1 

UNION ALL

SELECT *, 2 AS maquina
FROM MOBA.moba_2;


"""
    sql = pd.read_sql(query, connection)
    sql2 = pd.read_sql(query2, connection)
    connection.close()
    sql2['Data'] = pd.to_datetime(sql2['Data']).dt.date
    sql2 = sql2[sql2['Data'] == data_selecionada]
    sql2['hora'] = sql2['Hora'].astype(int)
    sql2 = sql2.drop([ 'Produção', 'Final', 'Crack', 'Tempo', 'Hora'], axis = 1)

    sql['Data'] = pd.to_datetime(sql['hour']).dt.date
    sql = sql[sql['Data'] == data_selecionada]
    sql['hora'] = pd.to_datetime(sql['hour']).dt.hour
    sql = sql.drop(['hour', 'Data'], axis = 1)
    sql = sql[['hora', 'Prod_MOBA']]
    d = pd.DataFrame({'hora': hora[1:],'Prod. Postura': derivada })
    d['hora'] = d['hora'].astype(int)
    #d['hora'] = d['hora'].astype(str)
    d_agrupado = d.groupby('hora', as_index=False)['Prod. Postura'].mean()
    xxx = pd.merge(d_agrupado, sql, how='left', on='hora')
    xxx = pd.merge(xxx, sql2, how='left', on='hora')
    xxx['Prod. Postura'] = xxx['Prod. Postura'].astype(int)
    xxx['Prod_MOBA'] = xxx['Prod_MOBA'].astype(int)
    xxx['Dif.'] =  xxx['Prod_MOBA'] - xxx['Prod. Postura']
    #xxx['Situação'] = xxx['Dif.'].apply(lambda x: 'ABASTECIMENTO' if x > 80 else 'OK')
    xxx = xxx[['hora', 'Prod_MOBA', 'Prod. Postura', 'Dif.', 'Parada', 'Detalhes', 'maquina']]
    xxx = xxx.sort_values(by='hora', ascending=True)

    st.dataframe(xxx, use_container_width= True, hide_index = True)
    #st.write(d)
    #st.write(sql)


with tabs[3]:

    tabs2 = st.tabs(["Status Contadores", "Ocorrências OFF"])
    # Filtrar os dados de status pela data selecionada
    with tabs2[0]:
        
        status_filtrados = status[status['Data'].dt.date == data_selecionada]

        if len(status_filtrados) == 0:
            st.write("Não há dados para este dia!")

        else:
            status_filtrados_temp = []  # Lista vazia inicialmente

            if opcao_colunas == 'Esteiras principais':
                status_filtrados_temp = list(status_filtrados.columns[1:9].intersection(status_filtrados.columns))  # Colunas da 2ª à 9ª
            elif opcao_colunas == 'POSTURA N1':
                status_filtrados_temp = list(status_filtrados.columns[9:29].intersection(status_filtrados.columns))  # Colunas da 10ª à 36ª
            elif opcao_colunas == 'POSTURA N2':
                status_filtrados_temp = list(status_filtrados.columns[29:].intersection(status_filtrados.columns))  # Colunas da 10ª à 36ª
            elif opcao_colunas == 'Todos os Galpões':
                status_filtrados_temp = list(status_filtrados.columns[9:].intersection(status_filtrados.columns))  # Colunas da 10ª à 36ª

        # Criar uma lista com os nomes das esteiras
            esteiras = status_filtrados_temp
        
            status_relevantes = status.copy()
            status_relevantes = status_relevantes[status_relevantes['Data'].dt.date == data_selecionada]
                
                # Função para extrair apenas 'ON' e 'OFF' da string de status
            def extract_status(text):
                if 'ON' in text:
                    return '🟢 ON'
                elif 'OFF' in text:
                    return '🔴 OFF'
                else:
                    return '⚪'
            status_relevantes['Data'] = status_relevantes['Data'].dt.strftime('%H:%M')
                # Aplicar a função à cópia do DataFrame com as colunas relevantes
            status_relevantes.iloc[:, 1:] = status_relevantes.iloc[:, 1:].map(extract_status)
                # Remover linhas com valores nulos, se necessário
            status_relevantes.dropna(inplace=True)
            status1 = status_relevantes.T
            status1.columns = status1.iloc[0]

                # Removendo a primeira linha (que agora é o cabeçalho)
            status1 = status1[1:]
            st.dataframe(status1)

            contagem_off_total = 0
            for coluna in status1.columns:
                contagem_off_total += status1[coluna].eq('🔴 OFF').sum()
            #
            # Número total de elementos no DataFrame
            total_elementos = status1.size
            
            # Calcular a divisão
            divisao = 100*(1 - contagem_off_total / total_elementos)
    

        with tabs2[1]:
        # Filtrar os dados de status pela data selecionada
            status_filtrados = status[status['Data'].dt.date == data_selecionada]
            
            status_filtrados_temp = []  # Lista vazia inicialmente
            
            if opcao_colunas == 'Esteiras principais':
                status_filtrados_temp = list(status_filtrados.columns[1:9].intersection(status_filtrados.columns))  # Colunas da 2ª à 9ª
            elif opcao_colunas == 'POSTURA N1':
                status_filtrados_temp = list(status_filtrados.columns[9:29].intersection(status_filtrados.columns))  # Colunas da 10ª à 36ª
            elif opcao_colunas == 'POSTURA N2':
                status_filtrados_temp = list(status_filtrados.columns[29:].intersection(status_filtrados.columns))  # Colunas da 10ª à 36ª
            elif opcao_colunas == 'Todos os Galpões':
                status_filtrados_temp = list(status_filtrados.columns[9:].intersection(status_filtrados.columns))  # Colunas da 10ª à 36ª
            
            # Criar uma lista com os nomes das esteiras
            esteiras = status_filtrados_temp
            leng = status_filtrados.size
            # Inicializar uma lista para armazenar as ocorrências de OFF
            ocorrencias_off = []
            
            # Iterar sobre os dados filtrados para extrair as ocorrências de OFF
            xis = 0
            for esteira in esteiras:
                # Verificar se há registros OFF para esta esteira
                registros_off = status_filtrados[(status_filtrados[esteira].str.split(' - ').str[0] == 'OFF')]
                if len(registros_off) > 0:
                    # Iterar sobre os registros OFF
                    xis = xis + len(registros_off)
                    for index, registro in registros_off.iterrows():
                        # Obter a hora do registro
                        hora_registro = registro['Data'].strftime('%H:%M')
                        # Obter a descrição completa do OFF
                        descricao_off = registro[esteira].split(' - ')[1]
                        # Adicionar a esteira, hora e descrição completa à lista de ocorrências
                        ocorrencias_off.append({'Esteira': esteira, 'Hora': hora_registro})
            lenoff = registros_off.size
            #confiabilidade = 100 - lenoff/leng*100
            if xis > 0:
                # Criar um DataFrame a partir da lista de ocorrências OFF
                df_ocorrencias_off = pd.DataFrame(ocorrencias_off)
                
                # Exibir o DataFrame com as ocorrências de OFF
                contagem_ocorrencias = df_ocorrencias_off['Esteira'].value_counts()
                
                # Exibir o título
                st.markdown(f"<h3 style='text-align: center;'>Ocorrências de contadores em OFF (dia: {data_selecionadinha})</h3>", unsafe_allow_html=True)
                
                # Iterar sobre cada esteira e criar um expander para cada uma
                for esteira, contagem in contagem_ocorrencias.items():
                    # Criar um expander para a esteira atual
                    with st.expander(f'{esteira} ({contagem} ocorrências em OFF)'):
                        # Filtrar os dados apenas para esta esteira
                        dados_esteira = df_ocorrencias_off[df_ocorrencias_off['Esteira'] == esteira]
                        
                        # Verificar se há dados para esta esteira
                        if not dados_esteira.empty:
                            # Exibir os dados para esta esteira
                            st.table(dados_esteira)
                        else:
                            # Se não houver dados, exibir uma mensagem indicando que não há ocorrências
                            st.write("Não há ocorrências para esta esteira.")
            else:
                st.write("Não há ocorrências.")



    
data_minima_date = min(datas_disponiveis)
data_maxima_date = max(datas_disponiveis)

data_minima_date = pd.Timestamp(data_minima_date)
data_maxima_date = pd.Timestamp(data_maxima_date)



with tabs[4]:
    tabsis = st.tabs(["HeatMap Fissura x Hora x MOBA", "Correlação Fissura x Galpão"])

    with tabsis[0]:
        cola, colb = st.columns(2)
        colu1, colu2, colu3 = st.columns(3)
        with colu1:
            st.write("")
        with colu2:
            on = st.toggle('Usar dados')
        with colu3:
            st.write("")
        with cola:
            if on:
                moba1 = st.file_uploader("Fazer o upload dos dados MOBA 1:")
                mobadb1 = pd.read_csv(moba1, delimiter=';', encoding='utf-8')
            else:
                mobadb1 = pd.read_csv('MOBA 1 (4).csv', delimiter=';', encoding='utf-8')

            if mobadb1 is not None:
                
                mobadb1 = mobadb1[mobadb1['Fissura'] != 0]
                
                # Convertendo a coluna 'Data' para datetime
                mobadb1['Data'] = pd.to_datetime(mobadb1['Data'], format='%m/%d/%Y')
                
                # Calculando a data mínima como a data máxima menos 15 dias
                data_minima_15dias = data_maxima_date - pd.Timedelta(days=15)
                
                # Filtrando os dados com base nos últimos 15 dias
                mobadb1 = mobadb1[(mobadb1['Data'] >= data_minima_15dias) & (mobadb1['Data'] <= data_maxima_date)]
                mobadb1 = mobadb1.query('Fissura >= 0 and Fissura <= 30')
                
                # Ordenando o DataFrame pela coluna 'Data'
                mobadb1 = mobadb1.sort_values(by='Data')
                
                # Convertendo a coluna 'Data' para o formato desejado
                mobadb1['Data'] = mobadb1['Data'].dt.strftime('%d/%m/%Y')
                
                pivot_table1 = mobadb1.pivot_table(index='Data', columns='Hora', values='Fissura', aggfunc="mean")
                
                # Convertendo o índice do pivot_table2 para o formato 'dd/mm/yyyy'
                pivot_table1.index = pd.to_datetime(pivot_table1.index, format = '%d/%m/%Y')
                # Ordenando o índice de forma crescente
                pivot_table1.sort_index(inplace=True)
                
        with colb:
            
            if on:
                moba2 = st.file_uploader("Fazer o upload dos dados MOBA 2:")
                mobadb2 = pd.read_csv(moba2, delimiter=';', encoding='utf-8')
            else:
                mobadb2 = pd.read_csv('MOBA 2 (4).csv', delimiter=';', encoding='utf-8')

            if mobadb2 is not None:
                
                mobadb2 = mobadb2[mobadb2['Fissura'] != 0]
                
                # Convertendo a coluna 'Data' para datetime
                mobadb2['Data'] = pd.to_datetime(mobadb2['Data'], format='%m/%d/%Y')
                
                # Calculando a data mínima como a data máxima menos 15 dias
                data_minima_15dias = data_maxima_date - pd.Timedelta(days=15)
                
                # Filtrando os dados com base nos últimos 15 dias
                mobadb2 = mobadb2[(mobadb2['Data'] >= data_minima_15dias) & (mobadb2['Data'] <= data_maxima_date)]
                mobadb2 = mobadb2.query('Fissura >= 0 and Fissura <= 30')
                
                # Ordenando o DataFrame pela coluna 'Data'
                mobadb2 = mobadb2.sort_values(by='Data')
                
                # Convertendo a coluna 'Data' para o formato desejado
                #mobadb2['Data'] = mobadb2['Data'].dt.strftime('%d/%m/%Y')
                mobadb2['Data'] = mobadb2['Data']
                pivot_table2 = mobadb2.pivot_table(index='Data', columns='Hora', values='Fissura', aggfunc="mean")
                
                # Convertendo o índice do pivot_table2 para o formato 'dd/mm/yyyy'
                pivot_table2.index = pd.to_datetime(pivot_table2.index, format = '%d/%m/%Y')
                # Ordenando o índice de forma crescente
                pivot_table2.sort_index(inplace=True)
              
        with st.expander("Gráficos de calor (Fissura x Hora x MOBA) - Últimos 15 dias"):
    
            if mobadb1 is not None:
                pivot_table1.index = pd.to_datetime(pivot_table1.index, format = '%d/%m/%Y')
                pivot_table1.reset_index(inplace=True)  # Redefine o índice transformando-o em uma coluna
                pivot_table1['Data'] = pivot_table1['Data'].dt.strftime('%d/%m/%Y') # Converte o formato da data na coluna
                mask_zero = pivot_table1 == 0
                
                pivot_table1.set_index('Data', inplace=True)
                fig1 = plt.figure(figsize=(15, 11))
                sns.heatmap(pivot_table1, annot=True, cmap="YlGnBu", vmin=2, vmax=30, fmt=".1f")
                plt.title("Heatmap Fissura - MOBA 1")
                st.pyplot(fig1)
                plt.close(fig1)

        
            if mobadb2 is not None:
                pivot_table2.index = pd.to_datetime(pivot_table2.index, format = '%d/%m/%Y')
                pivot_table2.reset_index(inplace=True)  # Redefine o índice transformando-o em uma coluna
                pivot_table2['Data'] = pivot_table2['Data'].dt.strftime('%d/%m/%Y') # Converte o formato da data na coluna
                pivot_table2.set_index('Data', inplace=True)
                fig2 = plt.figure(figsize=(15, 11))
                sns.heatmap(pivot_table2, annot=True, cmap="YlGnBu", vmin=2, vmax=30, fmt=".1f")
                plt.title("Heatmap Fissura - MOBA 2")
                st.pyplot(fig2)
                plt.close(fig2)

    with tabsis[1]:

        multi = '''Índice de correlação de -1 a 1, quanto mais próximo ao extremo maior relação as variáveis terão.  
        Quanto mais próximo de 1456,'''
        #st.markdown(multi)
        st.image('correlacao.jpg')
        data_min = st.number_input("Escolher a quantidade de dias anteriores a serem analisados:", min_value=0, max_value=30, step=1)


        mobadb1 = pd.read_csv('MOBA 1 (4).csv', delimiter=';', encoding='utf-8')
        mobadb1 = mobadb1[mobadb1['Fissura'] != 0]
        mobadb1['Data'] = pd.to_datetime(mobadb1['Data'], format='%m/%d/%Y')
        data_minima_15dias = data_maxima_date - pd.Timedelta(days=data_min)
        mobadb1 = mobadb1[(mobadb1['Data'] >= data_minima_15dias) & (mobadb1['Data'] <= data_maxima_date)]
        mobadb1 = mobadb1.query('Fissura >= 0 and Fissura <= 30')
        mobadb1 = mobadb1.sort_values(by='Data')
        mobadb1['Data'] = mobadb1['Data'].dt.strftime('%d/%m/%Y')
        pivot_table1 = mobadb1.pivot_table(index='Data', columns='Hora', values='Fissura', aggfunc='mean')
        pivot_table1.index = pd.to_datetime(pivot_table1.index, format = '%d/%m/%Y')
        pivot_table1.sort_index(inplace=True)

        mobadb2 = pd.read_csv('MOBA 2 (4).csv', delimiter=';', encoding='utf-8')
        mobadb2 = mobadb2[mobadb2['Fissura'] != 0]
        mobadb2['Data'] = pd.to_datetime(mobadb2['Data'], format='%m/%d/%Y')
        data_minima_15dias = data_maxima_date - pd.Timedelta(days=data_min)
        mobadb2 = mobadb2[(mobadb2['Data'] >= data_minima_15dias) & (mobadb2['Data'] <= data_maxima_date)]
        mobadb2 = mobadb2.query('Fissura >= 0 and Fissura <= 30')
        mobadb2 = mobadb2.sort_values(by='Data')
        mobadb2['Data'] = mobadb2['Data']
        pivot_table2 = mobadb2.pivot_table(index='Data', columns='Hora', values='Fissura', aggfunc='mean')
        pivot_table2.index = pd.to_datetime(pivot_table2.index, format = '%d/%m/%Y')
        pivot_table2.sort_index(inplace=True)
        
        
        mobadb2['Data'] = mobadb2['Data'].dt.strftime('%d/%m/%Y')
        #pivottable = mobadb1.append(mobadb2, ignore_index=True)
        pivottable1 = mobadb1
        pivottable2 = mobadb2
        pivottable1.drop(columns=['Final', 'Produção', 'Crack', 'Parada', 'Tempo', 'Detalhes'], inplace=True)
        pivottable2.drop(columns=['Final', 'Produção', 'Crack', 'Parada', 'Tempo', 'Detalhe'], inplace=True)
        
        datas = pd.date_range(end=pd.Timestamp.now().normalize(), periods=15)
        datas = [data.strftime('%d/%m/%Y') for data in datas]
        # Inicializar listas para armazenar os dados
        datas_repetidas = []
        valores_hi = []
        valores_hf = []
        
        # Gerar os valores para as colunas 'HI' e 'HF' para cada dia
        for data in datas:
            for hora_inicio in range(4, 25):
                datas_repetidas.append(data)
                valores_hi.append(hora_inicio)
                valores_hf.append(hora_inicio + 1)
        
        # Criar o DataFrame
        df = pd.DataFrame({'Data': datas_repetidas, 'HI': valores_hi, 'HF': valores_hf})

        valores_fissura1 = []
        valores_fissura2 = []

        # Iterar sobre as linhas do DataFrame 'df'
        for indice, linha in df.iterrows():
            # Obter a data e hora da linha atual do DataFrame 'df'
            data_df = linha['Data']
            hi_df = linha['HI']
            
            # Procurar a linha correspondente no DataFrame 'pivottable'
            linha_pivot1 = pivottable1[(pivottable1['Data'] == data_df) & (pivottable1['Hora'] == hi_df)]
            # Procurar a linha correspondente no DataFrame 'pivottable'
            linha_pivot2 = pivottable2[(pivottable2['Data'] == data_df) & (pivottable2['Hora'] == hi_df)]
            # Verificar se a linha foi encontrada
            if not linha_pivot1.empty:
                # Obter o valor de fissura da linha encontrada
                valor_fissura1 = linha_pivot1['Fissura'].values[0]
                valores_fissura1.append(valor_fissura1)
            else:
                # Caso não haja correspondência, atribuir NaN (ou outro valor desejado)
                valores_fissura1.append(0)
                
            if not linha_pivot2.empty:
                # Obter o valor de fissura da linha encontrada
                valor_fissura2 = linha_pivot2['Fissura'].values[0]
                valores_fissura2.append(valor_fissura2)
            else:
                # Caso não haja correspondência, atribuir NaN (ou outro valor desejado)
                valores_fissura2.append(0)
        
        # Adicionar os valores de fissura ao DataFrame 'df' como uma nova coluna
        df['Fissura MOBA2'] = valores_fissura2
        df['Fissura MOBA1'] = valores_fissura1
        dfmoba = df

        
        diferencas = []
        
        # Iterar sobre as linhas do DataFrame 'df'
        for indice, linha in df.iterrows():
            # Obter a data, HI e HF da linha atual do DataFrame 'df'
            data_df = linha['Data']
            hi_df = linha['HI']
            hf_df = linha['HF']
            
            # Converter a coluna 'Data' para o formato 'dd/mm/yyyy' temporariamente
            dados['Data_temp'] = dados['Data'].dt.strftime('%d/%m/%Y')
            
            # Filtrar as linhas correspondentes no DataFrame 'dados' usando a data
            linhas_dados = dados[dados['Data_temp'] == data_df]
            
            # Remover coluna temporária
            dados.drop(columns=['Data_temp'], inplace=True)
            
            # Calcular a hora com base na coluna 'Hora'
            linhas_dados = linhas_dados.copy()
            linhas_dados.loc[:, 'Hora'] = linhas_dados['Data'].dt.hour + linhas_dados['Data'].dt.minute / 60


            
            # Encontrar o menor valor depois de HI e o maior valor antes de HF para cada coluna de contagem
            variacao_por_coluna = linhas_dados[colunas_exibir_temp].apply(lambda x: calcular_variacao(x, hi_df, hf_df))
            variacao_por_coluna = variacao_por_coluna.apply(lambda x: max(0, x))
            total_variacao = variacao_por_coluna.sum()
    
            # Calcular o percentual de cada valor em relação ao total
            percentual_por_coluna = variacao_por_coluna / total_variacao * 100
            
            # Adicionar os resultados à lista
            diferencas.append(percentual_por_coluna)
        
        # Criar um DataFrame com as diferenças calculadas
        df_diferencas = pd.DataFrame(diferencas, columns=colunas_exibir_temp)
        
        # Concatenar os DataFrames 'df' e 'df_diferencas'
        df = pd.concat([df, df_diferencas], axis=1)
        
        # Exibir o DataFrame resultante
        number = st.number_input('Número crítico de Fissurado:')
        df = df.loc[(df['Fissura MOBA1'] > 0) & (df['Fissura MOBA2'] > 0)]
        dfx = df
        dfx.dropna() 
        if opfinal == "POSTURA N1":
            df1 = df.loc[(df['Fissura MOBA1'] > number) | (df['Fissura MOBA2'] > number)]
        else:
            df1 = df.loc[(df['Fissura MOBA2'] > number) | (df['Fissura MOBA1'] > number)]
        #st.dataframe(df)
        df1 = df1.dropna() 
        df1.drop(columns=['Data', 'HI', 'HF'], inplace=True)
        media1 = df1['Fissura MOBA1'].agg('mean')
        media2 = df1['Fissura MOBA2'].agg('mean')
        contar = df1['Fissura MOBA2'].count()
        
        co1, co2, co3 = st.columns(3)
        with co1:
            st.write(f"Média MOBA1: {media1:.1f}%")  # Exibir a contagem de dados
        
        with co2:
            st.write(f"Contagem: {contar} dados")  # Exibir a média da coluna MOBA1
            
        
        with co3:
            st.write(f"Média MOBA2: {media2:.1f}%")  # Exibir a média da coluna MOBA2
        
        
        df1['Fissura MOBA1'] = df1['Fissura MOBA1'].round().astype(int)
        df1['Fissura MOBA2'] = df1['Fissura MOBA2'].round().astype(int)

        
        coA, coB = st.columns(2)
        
        # Gráfico para Fissura MOBA1
        with coA:
            value_counts = df1['Fissura MOBA1'].value_counts().reset_index()
            value_counts.columns = ['Fissura MOBA 1', 'Frequência']
            
            # Criando o gráfico de frequência com Plotly
            fig = px.bar(value_counts, x='Fissura MOBA 1', y='Frequência')
            fig.update_layout(width=300, height=280, xaxis_title='Fissura MOBA 1', yaxis_title='Frequência')
            
            # Exibindo o gráfico
            st.plotly_chart(fig)
        
        # Gráfico para Fissura MOBA2
        with coB:
            value_counts = df1['Fissura MOBA2'].value_counts().reset_index()
            value_counts.columns = ['Fissura MOBA 2', 'Frequência']
            
            # Criando o gráfico de frequência com Plotly
            fig = px.bar(value_counts, x='Fissura MOBA 2', y='Frequência')
            fig.update_layout(width=300, height=280, xaxis_title='Fissura MOBA 2', yaxis_title='Frequência')
            
            # Exibindo o gráfico
            st.plotly_chart(fig)
        
        matriz_correlacao = df1.corr()

        if opfinal == "POSTURA N1":
            colunas_selecionadas = ['Fissura MOBA1']

        elif opfinal == "POSTURA N2":
            colunas_selecionadas = ['Fissura MOBA2']
        else:
            colunas_selecionadas = []    

        if not colunas_selecionadas:
            st.error("Selecionar a opção POSTURA N1 ou POSTURA N2 para mostrar o mapa de correlação")
        else:
            df_s = matriz_correlacao[colunas_selecionadas]
    
            df_s = df_s.iloc[2:]
            df_s = df_s.sort_values(by=colunas_selecionadas[0], ascending=False)
            
            with st.expander("Dados:"):
                st.dataframe(df1)
            
            with st.expander("Correlação Fissura x Esteiras Ligadas:"):
                #st.write(f"Confiabilidade do modelo: {divisao:.1f}% contadores ON")
                plty.figure(figsize=(10, 16))
                sns.heatmap(df_s, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
                plty.title('Mapa de Correlação')
                st.pyplot(plty)

