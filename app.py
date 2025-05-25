# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import datetime
import os

app = Flask(__name__)

# Página inicial (formulário)
@app.route('/')
def index():
    return render_template('index.html')

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario == 'sindico' and senha == '123':
            return redirect(url_for('dashboard_sindico'))
        elif usuario == 'portaria' and senha == '123':
            return redirect(url_for('dashboard_portaria'))
        else:
            return render_template('login.html', erro='Credenciais inválidas')
    return render_template('login.html')

# Painel do síndico
@app.route('/dashboard-sindico')
def dashboard_sindico():
    return render_template('dashboard-sindico.html')

# Painel da portaria
@app.route('/dashboard-portaria')
def dashboard_portaria():
    return render_template('dashboard-portaria.html')

# Página de relatórios (acessada pelo síndico)
@app.route('/relatorios')
def relatorios():
    dados = []
    if os.path.exists('dados.csv'):
        with open('dados.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                dados.append(row)
    return render_template('relatorios.html', dados=dados)

# Rota para receber os dados do formulário e salvar no CSV
@app.route('/enviar', methods=['POST'])
def enviar():
    nome = request.form['nome']
    cpf = request.form['cpf']
    placa = request.form['placa']
    apartamento = request.form['apartamento']
    vaga = request.form['vaga']
    datahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open('dados.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([nome, cpf, placa, apartamento, vaga, datahora])

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

