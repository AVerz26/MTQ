from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import mysql.connector
from datetime import datetime
from functools import wraps
import pytz

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mantiqueiramantiqueira'

mysql_config = {
    'host': 'localhost',  # Substitua pelo host do seu banco de dados
    'user': 'mantiqueira',       # Substitua pelo seu usuário do MySQL
    'password': 'mantiqueira',  # Substitua pela sua senha do MySQL
    'database': 'BD_EXP'
}



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:  # Verifica se o usuário está logado
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def authenticate_user(username, password):
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    conn = mysql.connector.connect(**mysql_config)
    cur = conn.cursor()
    cur.execute(query, (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

@app.before_request
def before_request():
    g.username = session.get('username')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Autenticar o usuário
        user = authenticate_user(username, password)
        if user:
            session['user_id'] = user[0]  # ID do usuário
            session['username'] = user[1]  # Nome de usuário

            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('menu'))
        else:
            flash('Usuário ou senha inválidos!', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

@app.route('/menu')
@login_required
def menu():
    return render_template('index.html')


# Função para salvar os dados no banco de dados
def save_to_db(area, data, placa, destino, placa_carreta, nome_do_motorista, transportadora, tipo_carga, responsavel):
    query = """INSERT INTO portaria (area, data, placa, situacao, data_entrar, data_finalizar, cliente_destino, placa_carreta, nome_do_motorista, transportadora, tipo_carga, responsavel)
               VALUES (%s, %s, %s, %s, NULL, NULL, %s, %s, %s, %s, %s, %s)"""
    values = (area, data, placa, 'Aguardando', destino, placa_carreta, nome_do_motorista, transportadora, tipo_carga, responsavel)
    conn = mysql.connector.connect(**mysql_config, autocommit=True)
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()
    cur.close()
    conn.close()

def save_to_db_motora(nome, placav, placac):
    query = """INSERT INTO motorista (nome, placav, placac)
               VALUES (%s, %s, %s)"""
    values = (nome, placav, placac)
    conn = mysql.connector.connect(**mysql_config, autocommit=True)
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()
    cur.close()
    conn.close()

# Função para ler os dados filtrados pela data de hoje
def read_today_data():
    today = datetime.now().strftime('%Y-%m-%d')
    query = "SELECT * FROM portaria WHERE DATE(data) = %s OR DATE(data) = DATE_SUB(%s, INTERVAL 1 DAY)"
    conn = mysql.connector.connect(**mysql_config, autocommit=True)
    cur = conn.cursor()
    cur.execute(query, (today,today))
    records = cur.fetchall()
    cur.close()
    conn.close()
    return records

# Função para atualizar a situação e as datas no banco de dados
def update_situation_in_db(id, situacao):
    query = """UPDATE portaria SET situacao = %s WHERE id = %s"""
    conn = mysql.connector.connect(**mysql_config, autocommit=True)
    cur = conn.cursor()
    cur.execute(query, (situacao, id))
    conn.commit()
    cur.close()
    conn.close()


def update_area_and_placa_in_db(area, placa, id, destino):
    if id is None or area is None or placa is None or destino is None:
        raise ValueError("Todos os parâmetros (id, area, placa, destino) devem ser fornecidos.")
    
    query = """UPDATE portaria SET area = %s, placa = %s, cliente_destino = %s WHERE id = %s"""
    conn = mysql.connector.connect(**mysql_config, autocommit=True)
    cur = conn.cursor()
    cur.execute(query, (area, placa, destino, id))
    conn.commit()
    cur.close()
    conn.close()

@app.route('/cadastro', methods=['GET', 'POST'], endpoint='cadastro')
@login_required
def index():
    if request.method == 'POST':
        area = request.form['area']
        data = request.form['data']
        placa = request.form['placa']
        destino = request.form['destino']
        placa_carreta = request.form['placa_carreta']
        nome_do_motorista = request.form['nome_do_motorista']
        transportadora = request.form['transportadora']
        tipo_carga = request.form['tipo_carga']
        responsavel = g.username

        # Salvar os dados no banco de dados
        save_to_db(area, data, placa, destino, placa_carreta, nome_do_motorista, transportadora, tipo_carga, responsavel)

        return redirect(url_for('cadastro'))
    utc_minus_4 = pytz.timezone('Etc/GMT+4')
    current_datetime = datetime.now(utc_minus_4).strftime('%Y-%m-%d %H:%M')
    return render_template('cadastro.html', current_datetime=current_datetime, username=g.username)

@app.route('/ocorrencia', methods=['GET', 'POST'], endpoint='ocorrencia')
@login_required
def ocorrencia():
    if request.method == 'POST':
        nome = request.form['nome']
        placav = request.form['placav']
        placac = request.form['placac']

        # Salvar os dados no banco de dados
        save_to_db_motora(nome, placav, placac)

        return redirect(url_for('ocorrencia'))
    return render_template('ocorrencia.html', username=g.username)

def update_data_entrar_in_db(id, data_entrar):
    query = """UPDATE portaria SET data_entrar = %s WHERE id = %s"""
    conn = mysql.connector.connect(**mysql_config, autocommit=True)
    cur = conn.cursor()
    cur.execute(query, (data_entrar, id))
    conn.commit()
    cur.close()
    conn.close()

def update_data_finalizar_in_db(id, data_finalizar):
    query = """UPDATE portaria SET data_finalizar = %s WHERE id = %s"""
    conn = mysql.connector.connect(**mysql_config, autocommit=True)
    cur = conn.cursor()
    cur.execute(query, (data_finalizar, id))
    conn.commit()
    cur.close()
    conn.close()

@app.route('/consultar', methods=['GET', 'POST'], endpoint='consultar')
@login_required
def consultar():
    records = read_today_data()
    editing = request.args.get('edit', 'false') == 'true'

    if request.method == 'POST':
        for record in records:
            # Atualizar situação
            situacao = request.form.get(f"situacao_{record[0]}")
            id = record[0]  # ID do registro
            placa = request.form.get(f"placa_{record[0]}")
            area = request.form.get(f"area_{record[0]}")
            destino = request.form.get(f"destino_{record[0]}")

            if id is None or placa is None or area is None or destino is None:

                continue

            if situacao:
                # Atualiza a situação e as datas no banco
                data_entrar = request.form.get(f"data_entrar_{record[0]}")
                data_finalizar = request.form.get(f"data_finalizar_{record[0]}")

                # Atualiza situação no banco
                update_situation_in_db(id, situacao)
                update_area_and_placa_in_db(area, placa, id, destino)

                # Se a situação for "Entrou", atualiza a data de entrada
                if situacao == 'Carregando' or situacao == 'Descarregando' and data_entrar:
                    update_data_entrar_in_db(id, data_entrar)
                
                # Se a situação for "Finalizado", atualiza a data de finalização
                if situacao == 'Finalizado' and data_finalizar:
                    update_data_finalizar_in_db(id, data_finalizar)

            



        # Recarregar registros para refletir as alterações
        return redirect(url_for('consultar', edit='false'))

    return render_template('consultar.html', records=records, editing=editing)



@app.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    print(id)
    query = "DELETE FROM portaria WHERE id = %s"
    conn = mysql.connector.connect(**mysql_config, autocommit=True)
    cur = conn.cursor()
    cur.execute(query, (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('consultar'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
