import telepot
import time
import schedule
import os
import io
from PIL import Image


TOKEN = '7645532925:AAGej49Otov39WJIXm0sGlC3RuAncErRbvU'
CHAT_ID = '988668946'

def concatenar_imagens(imagem1_path, imagem2_path, modo='horizontal'):
    img_byte_arr = io.BytesIO()
    imagem1 = Image.open(imagem1_path)
    imagem2 = Image.open(imagem2_path)

    if modo == 'horizontal':
        largura_total = imagem1.width + imagem2.width
        altura_maxima = max(imagem1.height, imagem2.height)
        nova_imagem = Image.new('RGB', (largura_total, altura_maxima))
        nova_imagem.paste(imagem1, (0, 0))
        nova_imagem.paste(imagem2, (imagem1.width, 0))
    elif modo == 'vertical':
        largura_maxima = max(imagem1.width, imagem2.width)
        altura_total = imagem1.height + imagem2.height
        nova_imagem = Image.new('RGB', (largura_maxima, altura_total))
        nova_imagem.paste(imagem1, (0, 0))
        nova_imagem.paste(imagem2, (0, imagem1.height))

    # Salvar a imagem concatenada no buffer de bytes
    nova_imagem.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)  # Voltar para o início do buffer
    return img_byte_arr


grafico_path = './grafana_images/grafico.png'
aca2_path = './grafana_images/aca.png'
caixas_path = './grafana_images/caixas.png'
aca_moba_path = './grafana_images/aca_moba.png'
hora_path = './grafana_images/hora.png'

bot = telepot.Bot(TOKEN)
def enviar_imagem(caminho_imagem):
    if isinstance(caminho_imagem, str):  # Se for um caminho de arquivo
        if os.path.exists(caminho_imagem):
            with open(caminho_imagem, 'rb') as f:
                bot.sendPhoto(chat_id=CHAT_ID, photo=f)
                print(f'Imagem enviada para o chat {CHAT_ID}.')
        else:
            print(f'Arquivo não encontrado: {caminho_imagem}')
    elif isinstance(caminho_imagem, io.BytesIO):  # Se for um objeto BytesIO
        try:
            caminho_imagem.seek(0)  # Voltar para o início do buffer
            bot.sendPhoto(chat_id=CHAT_ID, photo=caminho_imagem)
            print(f'Imagem enviada para o chat {CHAT_ID}.')
        except Exception as e:
            print(f'Erro ao enviar a imagem de BytesIO: {e}')
    else:
        print(f'Tipo de caminho inválido: {caminho_imagem}')

def handle_message(msg):
    command = msg['text']
    
    # Sempre recalcular as imagens concatenadas ao receber um comando
    if command == '/grafico':
        # Concatenar o gráfico
        grafico = concatenar_imagens(hora_path, grafico_path, modo='vertical')
        enviar_imagem(grafico)
    elif command == '/aca':
        # Concatenar o aca
        aca1 = concatenar_imagens(hora_path, aca2_path, modo='vertical')
        aca = concatenar_imagens(aca1, aca_moba_path, modo='vertical')
        enviar_imagem(aca)
    elif command == '/caixas':
        # Concatenar as caixas
        caixas = concatenar_imagens(hora_path, caixas_path, modo='vertical')
        enviar_imagem(caixas)
    else:
        bot.sendMessage(msg['chat']['id'], "Comando não reconhecido. Use /grafico, /aca ou /caixas.")

# Configurar o bot para ouvir as mensagens
bot.message_loop(handle_message)

print("Use /grafico, /aca ou /caixas.")

# Manter o bot rodando
while True:
    time.sleep(10)