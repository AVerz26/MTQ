import pandas as pd
import pymysql
from sqlalchemy import create_engine, text

import time

# Função para carregar os dados
def load_data(url):
    df = pd.read_csv(url)

    df.iloc[:, 2] = df.iloc[:, 2].replace({',': '.'}, regex=True).astype(float)
    df['Fissura'] = pd.to_numeric(df['Fissura'].replace({',': '.'}, regex=True), errors='coerce')
    df.iloc[:, 3] = df.iloc[:, 3].replace({',': '.'}, regex=True).astype(int)
    df['Produção'] = pd.to_numeric(df['Produção'].replace({',': '.'}, regex=True), errors='coerce')
    df.iloc[:, 4] = df.iloc[:, 4].replace({',': '.'}, regex=True).astype(int)
    df['Final'] = pd.to_numeric(df['Final'].replace({',': '.'}, regex=True), errors='coerce')
    df.iloc[:, 5] = df.iloc[:, 5].replace({',': '.'}, regex=True).astype(float)
    df['Crack'] = pd.to_numeric(df['Crack'].replace({',': '.'}, regex=True), errors='coerce')
    return df

# Função para verificar e inserir dados novos no MySQL
def check_and_insert_data():
    # URLs dos arquivos CSV
    url1 = "https://docs.google.com/spreadsheets/d/1HBKNz-SC1PKQlc3wy3fCjitQ9GvdfHD6/gviz/tq?tqx=out:csv" #moba 1
    url2 = "https://docs.google.com/spreadsheets/d/1AKAbGia97sMtwWjijmoB3wUslFyzacsN/gviz/tq?tqx=out:csv" #moba 2
    url3 = "https://docs.google.com/spreadsheets/d/1S0OvHr8BcY6SCW2MCGwt3gaHcjxGbLFBvVMVBT0iMpQ/gviz/tq?tqx=out:csv" #reprova qualidade
    
    # Carregar dados dos dois CSVs
    df1 = load_data(url1)
    df2 = load_data(url2)
    df3 = pd.read_csv(url3)
    df3['Data'] = pd.to_datetime(df3['Data'])
    
    
    
    # Conectar ao banco de dados MySQL
    engine = create_engine('mysql+pymysql://mantiqueira:mantiqueira@127.0.0.1:3306/MOBA')

    # Criar tabelas se não existirem
    with engine.connect() as conn:
        conn.execute(text('''CREATE TABLE IF NOT EXISTS moba_1 (
            Hora INT,
            Data DATE,
            Fissura DECIMAL(10, 2),
            Produção INT,
            Final INT,
            Crack DECIMAL(10, 2),
            Parada VARCHAR(255),
            Tempo INT,
            Detalhes VARCHAR(255),              
            PRIMARY KEY(Hora, Data, Fissura)
        );'''))
        conn.execute(text('''CREATE TABLE IF NOT EXISTS moba_2 (
            Hora INT,
            Data DATE,
            Fissura DECIMAL(10, 2),
            Produção INT,
            Final INT,
            Crack DECIMAL(10, 2),
            Parada VARCHAR(255),
            Tempo INT,
            Detalhes VARCHAR(255),              
            PRIMARY KEY(Hora, Data, Fissura)
        );'''))

        conn.execute(text('''CREATE TABLE IF NOT EXISTS reprova (
            Item VARCHAR(10),
            Quantidade INT,
            Unidade VARCHAR(10),
            Data TIMESTAMP,
            Motivo VARCHAR(255),
            Local VARCHAR(255),
            Turno VARCHAR(3),            
            PRIMARY KEY(Data)
        );'''))


    # Sobrescrevendo os dados na tabela moba_1
    with engine.connect() as conn:
        df1.to_sql('moba_1', conn, if_exists='replace', index=False)
        print(f'{len(df1)} dados inseridos na tabela reprova, substituindo os dados existentes.')
        df2.to_sql('moba_2', conn, if_exists='replace', index=False)
        print(f'{len(df2)} dados inseridos na tabela reprova, substituindo os dados existentes.')
        df3.to_sql('reprova', conn, if_exists='replace', index=False)
        print(f'{len(df3)} dados inseridos na tabela reprova, substituindo os dados existentes.')


    df1['Data'] = pd.to_datetime(df1['Data']).dt.strftime('%m/%d/%Y')
    df2['Data'] = pd.to_datetime(df2['Data']).dt.strftime('%m/%d/%Y')
    df1.to_csv('MOBA 1 (4).csv', sep=";", index=False, encoding='utf-8')
    
    df2.to_csv('MOBA 2 (4).csv', sep=";", index=False, encoding='utf-8')

# Loop de execução contínua
for i in range(1,1440000):
    check_and_insert_data()
    time.sleep(3600)  # Espera 1 hora entre as verificações
