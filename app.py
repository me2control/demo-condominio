# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os

app = Flask(__name__)
app.secret_key = 'me2-secret-key'  # Necessário para usar flash messages

CAMINHO_ARQUIVO = 'dados.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        placa = request.form['placa']
        apartamento = request.form['apartamento']
        vaga = request.form['vaga']
        motivo = request.form['motivo']

        if not all([nome, cpf, placa, apartamento, vaga, motivo]):
            flash("Todos os campos são obrigatórios.")
            return redirect(url_for('index'))

        novo_registro = [nome, cpf, placa, apartamento, vaga, motivo]

        novo_arquivo = not os.path.exists(CAMINHO_ARQUIVO)

        with open(CAMINHO_ARQUIVO, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if novo_arquivo:
                writer.writerow(['Nome', 'CPF', 'Placa', 'Apartamento', 'Vaga', 'Motivo'])
            writer.writerow(novo_registro)

        return render_template('cadastro_sucesso.html', nome=nome)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def autenticar():
    usuario = request.form['usuario']
    senha = request.form['senha']

    if usuario == 'sindico' and senha == 'admin':
        return redirect(url_for('dashboard_sindico'))
    elif usuario == 'portaria' and senha == '1234':
        return redirect(url_for('portaria'))
    else:
        flash('Usuário ou senha incorretos.')
        return redirect(url_for('login'))

@app.route('/sindico')
def dashboard_sindico():
    return render_template('dashboard-sindico.html')

@app.route('/portaria')
def portaria():
    return render_template('portaria.html')

@app.route('/relatorios')
def relatorios():
    registros = []
    if os.path.exists(CAMINHO_ARQUIVO):
        with open(CAMINHO_ARQUIVO, mode='r', encoding='utf-8') as file:
            leitor = csv.reader(file)
            cabecalho = next(leitor, None)
            for linha in leitor:
                registros.append(linha)
    return render_template('relatorios.html', registros=registros)

if __name__ == '__main__':
    app.run(debug=True)

