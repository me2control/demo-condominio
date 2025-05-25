# app.py
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os

app = Flask(__name__)
app.secret_key = 'me2-system-secret'

CSV_FILE = 'dados.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        documento = request.form['documento']
        apartamento = request.form['apartamento']
        motivo = request.form['motivo']

        if not motivo:
            return "Por favor, selecione o motivo da visita.", 400

        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([nome, documento, apartamento, motivo])

        return render_template('obrigado.html', nome=nome)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = request.form['usuario']
    senha = request.form['senha']

    if usuario == 'sindico' and senha == 'sindico123':
        session['usuario'] = 'sindico'
        return redirect(url_for('dashboard_sindico'))
    elif usuario == 'portaria' and senha == 'portaria123':
        session['usuario'] = 'portaria'
        return redirect(url_for('relatorios'))
    else:
        return render_template('login.html', erro='Usuário ou senha inválidos.')

@app.route('/dashboard-sindico')
def dashboard_sindico():
    if session.get('usuario') == 'sindico':
        return render_template('dashboard-sindico.html')
    return redirect(url_for('login'))

@app.route('/relatorios')
def relatorios():
    if session.get('usuario') == 'portaria':
        registros = []
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                registros = list(reader)
        return render_template('dashboard_portaria.html', registros=registros)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

