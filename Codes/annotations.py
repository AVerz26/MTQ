import time
import requests
import mysql.connector
import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="mantiqueira",
    password="mantiqueira", 
    database="grafana_data"  
)
cursor = conn.cursor()

api_url = "http://192.168.5.5:3000/api/annotations"
headers = {"Authorization": "Bearer glsa_wBVLeWhAVxMr5ZRSj3Sjl2cmqkEMQgUH_722059e0"}
params = {"from": 1733252422119, "to": 2400000000000}

def consultar_e_inserir():
    response = requests.get(api_url, headers=headers, params=params)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        annotations = response.json()

        for annotation in annotations:
            start_time = annotation['time']
            end_time = annotation.get('timeEnd', start_time)
            tag = ', '.join(annotation['tags']) if 'tags' in annotation else ''
            description = annotation['text']

            # Converter 'start_time' de milissegundos para timestamp legível
            timestamp = datetime.datetime.fromtimestamp(start_time / 1000)  # Conversão para datetime

            # Verificar se a anotação já existe no banco de dados (baseado no 'start_time')
            cursor.execute("""
                SELECT descricao FROM paradas WHERE start_time = %s
            """, (start_time,))
            result = cursor.fetchone()

            if result is not None:  # Se a anotação já existir
                existing_description = result[0]

                # Se a descrição mudou, atualizar a linha
                if existing_description != description:
                    cursor.execute("""
                        UPDATE paradas
                        SET descricao = %s, end_time = %s, tag = %s, times = %s
                        WHERE start_time = %s
                    """, (description, end_time, tag, timestamp, start_time))
                    conn.commit()
                    #print(f"Anotação atualizada: {description} (start_time: {start_time}, timestamp: {timestamp})")

            else:
                # Caso a anotação não exista, inserir nova linha
                cursor.execute("""
                    INSERT INTO paradas (start_time, end_time, tag, descricao, times)
                    VALUES (%s, %s, %s, %s, %s)
                """, (start_time, end_time, tag, description, timestamp))
                conn.commit()
                #print(f"Anotação inserida: {description} (start_time: {start_time}, timestamp: {timestamp})")

    else:
        print(f"Erro ao acessar a API. Código de status: {response.status_code}")

import time
while True:
    consultar_e_inserir()  
    time.sleep(600) 