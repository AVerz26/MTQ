import telepot
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
from tqdm import tqdm
import requests
from github import Github
from sqlalchemy import create_engine, text
import hashlib
from telepot.loop import MessageLoop
import re
import os
from selenium.common.exceptions import NoSuchElementException
import resource 


def get_data_and_classify(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot.sendChatAction(chat_id, 'typing')
    
    try:
        organizations_and_csv = {'211': '1',
                             "421": '2', 
                             "908": '3', 
                             "38": '4', 
                             "896": '5',
                             "219": '6',
                             "902": '7',
                             "887": '8',
                             "2287": '9'}

        last_values = {}
        results = []
        t1 = time.time()
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")
        options.add_argument('--single-process') 
        driver = webdriver.Chrome(options=options)

        username = 'mtq-ms'
        password = 'mtq-ms2017'

        url = 'https://sistema.kajoo.com.br/'
        driver.get(url)
        time.sleep(40)
        driver.find_element(By.ID, 'input_0').send_keys(username)
        driver.find_element(By.ID, 'input_1').send_keys(password, Keys.RETURN)
        time.sleep(40)

        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
        historical_data = {}
        historical = {}
        organization_data = {}

        total_organizations = len(organizations_and_csv)

        message = bot.sendMessage(chat_id, "Iniciando processamento...\n`[░░░░░░░░░░░░░░░░░░░░░░░░░░░░]`", parse_mode='Markdown')
        message_id = message['message_id']

        for idx, (org_id, csv_path) in enumerate(tqdm(organizations_and_csv.items(), desc="Progresso", position=0, leave=False)):
            if idx > 0:  # Ignora a primeira iteração, pois a primeira aba já foi aberta
                driver.execute_script("window.open('');")  # Abre uma nova aba
            driver.switch_to.window(driver.window_handles[idx])
            new_url = f'https://sistema.kajoo.com.br/#/admin/statistics?organization_id={org_id}'
            driver.get(new_url)
            #driver.execute_script(f"window.location.href = '{new_url}';")
            driver.execute_script("location.reload();")
            time.sleep(35)
            driver.find_element(By.XPATH, '//button[@ng-click="vm.openStatisticsTable()"]').click()
            time.sleep(15)
            table = driver.find_element(By.XPATH, '//*[@id="statistics-table"]/md-content/div[2]')
            table_data = [[cell.text for cell in row.find_elements(By.TAG_NAME, 'td')] for row in table.find_elements(By.TAG_NAME, 'tr')]

            for i in range(1, len(table_data)):
                for j in range(len(table_data[i])):
                    if table_data[i][j] == '':
                        table_data[i][j] = 0  
                        try:
                            table_data[i][j] = int(table_data[i][j])
                        except ValueError:
                            table_data[i][j] = 0  

            hist_df = pd.DataFrame(table_data[1:]).iloc[:, :-2]
            org_df = pd.DataFrame(table_data[1:]).iloc[:, [-1]]
            org_df.columns = [""]
            historical_data[org_id] = hist_df.T
            organization_data[org_id] = org_df.T

            current_progress = idx + 1
            progress = int((current_progress / total_organizations) * 20)
            enviar_mensagem_com_barra_de_progresso(chat_id, message_id, progress, org_id)

        mensagem_conclusao = "Concluído!\n`[████████████████████████]` (100%)"
        bot.editMessageText((chat_id, message_id), mensagem_conclusao, parse_mode='Markdown')
    
        combined_data = pd.concat(organization_data, axis=1)
        historico_data = pd.concat(historical_data, axis=1)



        combined_data.insert(0, 'Hora', timestamp)

        #new_url = f'https://sistema.kajoo.com.br/#/admin/terminal/dashboard'
       # driver.get(new_url)
        #driver.execute_script(f"window.location.href = '{new_url}';")
        #driver.execute_script("location.reload();")
        #time.sleep(20)
    
        #nome_galpoes = []
        #for i in range(1, 9):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[2]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div/span'
        #    element = driver.find_element(By.XPATH, xpath)
        #    nome_galpoes.append(element.text)
        #for i in range(1, 6):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[3]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div/span'
        #    element = driver.find_element(By.XPATH, xpath)
        #    nome_galpoes.append(element.text)
        #for i in range(1, 6):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[4]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div/span'
        #    element = driver.find_element(By.XPATH, xpath)
        #    nome_galpoes.append(element.text)
        #for i in range(1, 6):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[5]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div/span'
        #    element = driver.find_element(By.XPATH, xpath)
        #    nome_galpoes.append(element.text)
        #for i in range(1, 6):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[6]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div/span'
        #    element = driver.find_element(By.XPATH, xpath)
        #    nome_galpoes.append(element.text)
        #for i in range(1, 6):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[7]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div/span'
        #    element = driver.find_element(By.XPATH, xpath)
        #    nome_galpoes.append(element.text)  
        #for i in range(1, 6):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[8]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div/span'
        #    element = driver.find_element(By.XPATH, xpath)
        #    nome_galpoes.append(element.text)
        #for i in range(1, 9):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[9]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div/span'
        #    element = driver.find_element(By.XPATH, xpath)
        #    nome_galpoes.append(element.text)
        #for i in range(1, 3):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[10]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div/span'
        #    element = driver.find_element(By.XPATH, xpath)
        #    nome_galpoes.append(element.text)
    
    
        #status_elements = []
        #for i in range(1, 9):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[2]/div[2]/div[{i}]/div[2]/div[1]/div[1]'
        #    element = driver.find_element(By.XPATH, xpath)
        #    status_elements.append(element.text)
        #for i in range(1, 6):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[3]/div[2]/div[{i}]/div[2]/div[1]/div[1]'
        #    element = driver.find_element(By.XPATH, xpath)
        #    status_elements.append(element.text)
        #for i in range(1, 6):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[4]/div[2]/div[{i}]/div[2]/div[1]/div[1]'
        #    element = driver.find_element(By.XPATH, xpath)
        #    status_elements.append(element.text)
        #for i in range(1, 6):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[5]/div[2]/div[{i}]/div[2]/div[1]/div[1]'
        #    element = driver.find_element(By.XPATH, xpath)
        #    #status_elements.append(element.text)
        #    try:
        #        element = driver.find_element(By.XPATH, xpath)
        #        status_elements.append(element.text)
        #    except NoSuchElementException:
        #       status_elements.append('OFF')
        #for i in range(1, 6):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[6]/div[2]/div[{i}]/div[2]/div[1]/div[1]'
        #   element = driver.find_element(By.XPATH, xpath)
        #   status_elements.append(element.text)
        #for i in range(1, 6):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[7]/div[2]/div[{i}]/div[2]/div[1]/div[1]'
        #    element = driver.find_element(By.XPATH, xpath)
        #    status_elements.append(element.text)  
        #for i in range(1, 6):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[8]/div[2]/div[{i}]/div[2]/div[1]/div[1]'
        #    element = driver.find_element(By.XPATH, xpath)
        #    status_elements.append(element.text)
        #for i in range(1, 9):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[9]/div[2]/div[{i}]/div[2]/div[1]/div[1]'
        #    element = driver.find_element(By.XPATH, xpath)
        #    status_elements.append(element.text)
        #for i in range(1, 3):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[10]/div[2]/div[{i}]/div[2]/div[1]/div[1]'
        #    element = driver.find_element(By.XPATH, xpath)
        #    status_elements.append(element.text)
        
        
        
# Encontrar os elementos que contêm o tempo desde
       # time_since_elements = []
    
        #for i in range(1, 9):
        #    xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[2]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/span/time-since/span'
        #    element = driver.find_element(By.XPATH, xpath)
        #    time_since_elements.append(element.text)
       # 
       # for i in range(1,6):    
       #     xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[3]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/span/time-since/span'
       #     element = driver.find_element(By.XPATH, xpath)
       #     time_since_elements.append(element.text)
       # for i in range(1,6):    
       #     xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[4]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/span/time-since/span'
       #     element = driver.find_element(By.XPATH, xpath)
       #     time_since_elements.append(element.text)
       # for i in range(1,6):    
       #     xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[5]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/span/time-since/span'
       #     element = driver.find_element(By.XPATH, xpath)
       #     time_since_elements.append(element.text)
       #     try:
       #         element = driver.find_element(By.XPATH, xpath)
       #         time_since_elements.append(element.text)
       #     except NoSuchElementException:
       #         time_since_elements.append('0')
       # for i in range(1,6):    
       #     xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[6]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/span/time-since/span'
       #     element = driver.find_element(By.XPATH, xpath)
       #     time_since_elements.append(element.text)
       # for i in range(1,6):    
       #     xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[7]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/span/time-since/span'
       #     element = driver.find_element(By.XPATH, xpath)
       #     time_since_elements.append(element.text)
       # for i in range(1,6):    
       #     xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[8]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/span/time-since/span'
       #     element = driver.find_element(By.XPATH, xpath)
       #     time_since_elements.append(element.text)
       # for i in range(1,9):    
       #     xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[9]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/span/time-since/span'
       #     element = driver.find_element(By.XPATH, xpath)
       #     time_since_elements.append(element.text)
       # for i in range(1,3):    
       #     xpath = f'//*[@id="terminals-list-dashboard"]/md-content/section[10]/div[2]/div[{i}]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/span/time-since/span'
       #     element = driver.find_element(By.XPATH, xpath)
       #     time_since_elements.append(element.text)
       # 
        #time_since_elements = [time.split()[:2] for time in time_since_elements]



    # Criar um DataFrame com os valores extraídos
        #data = {'Nome Galpões': nome_galpoes, 'Status': [f'{status} - {time_since}' for status, time_since in zip(status_elements, time_since_elements)]}

       # df = pd.DataFrame(data)
       # df = df.T
       # df.columns = df.iloc[0]  # Definir os cabeçalhos das colunas como os valores da primeira linha
       # df = df.iloc[1:]  # Remover a primeira linha que agora é o cabeçalho
       # df.insert(0, 'Hora', timestamp)

        #engine = create_engine('mysql+pymysql://mantiqueira:mantiqueira@127.0.0.1:3306/BD_EXP')
        #with engine.connect() as conn:
        #    combined_data.to_sql('dados_esteira', conn, if_exists='append', index=False)

        
       # with open('StatusEST.csv', 'a', newline='') as f:
       #     df.to_csv(f, header=False, index=False, sep=';', encoding='utf-8')
 

        with open('HistoricalData.csv', 'w', newline='') as f:
            historico_data.to_csv(f, header=False, index=False, sep=';', encoding='utf-8')

        with open('Historico_BI.csv', 'w', newline='') as f:
            historico_data.to_csv(f, header=False, index=False, sep=';', encoding='utf-8')
        
        with open('Combinado_BI.csv', 'a', newline='') as f:
            combined_data.to_csv(f, header=False, index=False, sep=';', encoding='utf-8')

        with open('CombinedData.csv', 'w', newline='') as f:
            combined_data.to_csv(f, header=False, index=False, sep=';', encoding='utf-8')

        tk = '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'
        g = Github(tk)

        owner = "AVerz26"
        repo_name = "WS"

        file_path = "Combinado_BI.csv"
        file_path2 = "StatusEST.csv"

        with open(file_path, 'r') as file:
            file_content = file.read()
            
        with open(file_path2, 'r', encoding='ISO-8859-1') as file:
            file_content2 = file.read()

        sha_content = hashlib.sha1(file_content.encode()).hexdigest()
        sha_content2 = hashlib.sha1(file_content2.encode()).hexdigest()

        repo = g.get_user(owner).get_repo(repo_name)

        try:
            file = repo.get_contents(file_path)
            sha_base = file.sha
            file2 = repo.get_contents(file_path2)
            sha_base2 = file2.sha
        except:
            sha_base = None
            sha_base2 = None

        if sha_base is not None:
            contents = repo.update_file(file_path, "Atualizando arquivo CSV", file_content, sha_base, branch="main")
        else:
            contents = repo.create_file(file_path, "Adicionando arquivo CSV", file_content, branch="main")
        if sha_base2 is not None:
            contents = repo.update_file(file_path2, "Atualizando arquivo CSV", file_content2, sha_base2, branch="main")
        else:
            contents = repo.create_file(file_path2, "Adicionando arquivo CSV", file_content2, branch="main")   
        memoria_usada = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        memoria_usada_mb = memoria_usada / 1024
        driver.quit()

        #print(f'Banco de dados atualizado às {time.strftime("%H:%M:%S", time.localtime(t1))} com total de {int((time.time() - t1))} segundos.')
        mensagem = f'BD atualizado: {time.strftime("%H:%M:%S", time.localtime(t1))} em {int(time.time() - t1)} segundos. \n Memória sistema: {int(memoria_usada_mb)} MB'   
        
        time.sleep(1)
        bot.editMessageText((chat_id, message_id), mensagem, parse_mode='Markdown')
        zero = 1
        return combined_data, historico_data, mensagem, 1
    except Exception as e:
        error_message = str(e)  
        error_message = re.sub(r'http[s]?://\S+', '', error_message)
        error_message = error_message.split('\n')[0]
        enviar_mensagem(f"Ocorreu um erro: {error_message}")
        driver.quit()
        zero = 0
        tentativa = 0
        twt = 0
        current_time = datetime.now()
        current_hour = current_time.hour
        while zero == 0:
            x, y, z, zero = get_data_and_classify(msg)
            bot.sendMessage(chat_id, f"Resultado: {zero} às {current_hour} horas")

            if current_hour < 22:
                while zero == 0:
                    twt += 1        
                    bot.sendMessage(chat_id, f"Tentando novamente...{twt}")
                    x, y, z, zero = get_data_and_classify(msg)
                            
                    if zero == 0:                           
                        time.sleep(5)  # Aguarda 5 segundos antes de tentar novamente
                
                    # Se a hora for maior ou igual a 22, faz no máximo 3 tentativas
            else:
                zero = 0
                while zero == 0 and tentativa < 3:
                    x, y, z, zero = get_data_and_classify(msg)
                            
                    if zero == 0:
                        tentativa += 1
                        bot.sendMessage(chat_id, f"Tentativa {tentativa}/3 falhou. Tentando novamente...")
                        time.sleep(5)  # Aguarda 5 segundos antes de tentar novamente

                        
                        # Se falhou após 3 tentativas, aguarda até as 3:30 AM
                if zero == 0:
                    bot.sendMessage(chat_id, "Falha após 3 tentativas. Esperando até as 03:30 AM para tentar novamente...")
                    time.sleep(60*24*5)  # Espera até as 3:30 AM
            
        return combined_data, historico_data, mensagem, 0


def enviar_mensagem(texto):
    TELEGRAM_BOT_TOKEN = '6796154017:AAGCrvuynsYpsNdkWCgpjw8l_zNO0Lqqufg'
    CHAT_ID = '988668946'
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    params = {'chat_id': CHAT_ID, 'text': texto}
    requests.post(url, params=params)

def enviar_mensagem_com_barra_de_progresso(chat_id, message_id, progress, org_id):
    org = {
    '211': 'Est. P',
    '421': 'Est. 1',
    '908': 'Est. 7',
    '38': 'Est. 13',
    '896': 'Est. 19',
    '219': 'Est. 24',
    '902': 'Est. 31',
    '887': 'Est. 37',
    '2287': 'Est. 46'
}
    bar_length = 20
    progress_bar = "█" * progress + "░" * (bar_length - progress)
    mensagem = f"Leitura da {org.get(org_id)} realizada!\n`[{progress_bar}]` ({progress * (100 // bar_length)}%)"
    bot.editMessageText((chat_id, message_id), mensagem, parse_mode='Markdown')

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text' and msg['text'] == '/executar':
        for i in range(1, 1440000): 
            start_time = time.time()

            try:
                x, y, z, zero = get_data_and_classify(msg)

                elapsed_time = time.time() - start_time
                if elapsed_time < 600:
                    time.sleep(600 - elapsed_time)  
                else:
                    time.sleep(10) 

            except Exception as e:

                time.sleep(5)  

token = '8180183101:AAFvV665GTw97iZVlOr5C_VLWhq0KHTZKvU'

bot = telepot.Bot(token)

MessageLoop(bot, {'chat': handle}).run_as_thread()

while True:
    pass