from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey' 

csv_file_path = 'registros.csv'

def save_to_csv(area, data, placa):
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([area, data, placa, 'Aguardando', '', ''])  # Colunas: área, data, placa, situação, data_entrar, data_finalizar

# Função para ler os dados do CSV filtrados pela data de hoje
def read_today_data():
    today = datetime.now().strftime('%Y-%m-%d')
    records = []

    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1].startswith(today):  # Verifica se a data da linha é de hoje
                    records.append(row)
    except FileNotFoundError:
        pass  # Se o arquivo não existir, retornamos uma lista vazia
    
    return records

# Função para atualizar a situação e as datas no CSV
def update_situation_in_csv(data, situacao):
    rows = []
    updated = False
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)

        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            for row in rows:
                if row[1] == data:  # Verifica se a data da linha corresponde
                    if situacao == 'Entrou' and row[4] == '':  # Se for a primeira vez que mudou para 'Entrou'
                        row[4] = current_datetime  # Atualiza a data_entrar
                    elif situacao == 'Finalizado' and row[5] == '':  # Se for a primeira vez que mudou para 'Finalizado'
                        row[5] = current_datetime  # Atualiza a data_finalizar
                    row[3] = situacao  # Atualiza a situação
                    updated = True
                writer.writerow(row)
    except FileNotFoundError:
        pass

    return updated

# Função para editar os campos de "Área" e "Placa"
def update_area_and_placa_in_csv(data, area, placa):
    rows = []
    updated = False

    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)

        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            for row in rows:
                if row[1] == data:  # Verifica se a data da linha corresponde
                    row[0] = area  # Atualiza a área
                    row[2] = placa  # Atualiza a placa
                    updated = True
                writer.writerow(row)
    except FileNotFoundError:
        pass

    return updated

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        area = request.form['area']
        data = request.form['data']
        placa = request.form['placa']

        # Salvar os dados no CSV
        save_to_csv(area, data, placa)

        return redirect(url_for('index'))

    # Data atual no formato YYYY-MM-DD HH:MM:SS
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('index.html', current_datetime=current_datetime)

@app.route('/consultar', methods=['GET', 'POST'])
def consultar():
    records = read_today_data()
    editing = request.args.get('edit', 'false') == 'true'

    if request.method == 'POST':
        for record in records:
            situacao = request.form.get(f"situacao_{record[1]}")
            if situacao:
                update_situation_in_csv(record[1], situacao)

        for record in records:
            area = request.form.get(f"area_{record[1]}")
            placa = request.form.get(f"placa_{record[1]}")
            if area and placa:
                update_area_and_placa_in_csv(record[1], area, placa)

        records = read_today_data()

    return render_template('consultar.html', records=records, editing=editing)

@app.route('/excluir/<data>', methods=['POST'])
def excluir(data):
    rows = []
    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            rows = [row for row in reader if row[1] != data]  # Exclui a linha com a data especificada

        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
    except FileNotFoundError:
        pass
    return redirect(url_for('consultar'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")