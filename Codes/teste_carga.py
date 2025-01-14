from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurar o driver do Selenium
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Defina o número de repetições
n = 80  # Troque pelo número de vezes que você quer repetir a operação

# URL do site que você quer acessar
url = 'http://192.168.5.5:8501/'  # Altere para o site desejado
ne = 0
try:
    for _ in range(n):
        ne += 1
        print(+ne)
        driver.get(url)

        # Espera até que o campo de entrada esteja visível e preenche
        try:
            input_element = WebDriverWait(driver, 3).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="text_input_1"]'))
)

            input_element.clear()  # Limpa o campo antes de preencher
            input_element.send_keys('mq45812131')  # Texto que você quer preencher
        except Exception as e:
            continue  # Pula para a próxima iteração se não conseguir encontrar o campo

        # Espera até que o botão esteja clicável e clica
        try:
            button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/div[1]/div/div/div/section/div[1]/div/div/div/div[3]/div[1]/div/div/div/div[5]/div/div/div/div[2]/div/div/button'))
            )
            button.click()
        except Exception as e:
            print("Erro ao encontrar ou clicar no botão:", e)
        time.sleep(2)

finally:
    driver.quit()  # Fecha o navegador após completar as operações
