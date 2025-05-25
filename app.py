from flask import Flask, render_template, request, redirect, url_for, session, flash
import csv
import os

app = Flask(__name__)
app.secret_key = 'sb'\x9f\x1a\xdc\x0b\xeb\xe4\xf1\xf3\x82\x12\x17\x9c\xaf\xdb\x06\xc9\x8d\xbc\x14\xca\x81\xd3\xb4\xfd''  # Troque para algo seguro em produção

# Dados básicos para personalização (exemplo)
COND_NOME = "Demo Condomínio"
COND_LOGO = "/static/logo.png"
COND_CORES = {
    "cor1": "#1E88E5",  # azul primário
    "cor2": "#1565C0",
    "cor3": "#90CAF9"
}

# Usuários cadastrados (exemplo, ideal salvar em banco ou arquivo seguro)
USUARIOS = {
    "sindico": "senha123",
    "portaria": "senha123"
}

DADOS_CSV = 'dados.csv'

# Cria CSV com cabeçalho se não existir
if not os.path.exists(DADOS_CSV):
    with open(DADOS_CSV, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Nome', 'CPF', 'Placa', 'Apartamento', 'Vaga'])


@app.route('/')
def index():
    return render_template('index.html', nome=COND_NOME, logo=COND_LOGO, cores=COND_CORES)


@app.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    placa = request.form.get('placa')
    apartamento = request.form.get('apartamento')
    vaga = request.form.get('vaga')

    # Salva dados no CSV
    with open(DADOS_CSV, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([nome, cpf, placa, apartamento, vaga])

    # Mensagem de sucesso via renderização de página confirmacao.html
    return render_template('confirmacao.html', mensagem="Cadastro atualizado com sucesso!", nome=COND_NOME, logo=COND_LOGO, cores=COND_CORES)


@app.route('/login')
def login():
    return render_template('login.html', erro=None, nome=COND_NOME, logo=COND_LOGO, cores=COND_CORES)


@app.route('/login_usuario', methods=['POST'])
def login_usuario():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')

    # Validação simples
    if usuario in USUARIOS and USUARIOS[usuario] == senha:
        session['usuario'] = usuario
        if usuario == 'sindico':
            return redirect(url_for('dashboard_sindico'))
        elif usuario == 'portaria':
            return redirect(url_for('dashboard_portaria'))
    else:
        return render_template('login.html', erro="Usuário ou senha incorretos.", nome=COND_NOME, logo=COND_LOGO, cores=COND_CORES)


@app.route('/dashboard_sindico')
def dashboard_sindico():
    if 'usuario' not in session or session['usuario'] != 'sindico':
        flash('Acesso negado. Faça login como síndico.')
        return redirect(url_for('login'))

    return render_template('dashboard_sindico.html', nome=COND_NOME, logo=COND_LOGO, cores=COND_CORES)


@app.route('/dashboard_portaria')
def dashboard_portaria():
    if 'usuario' not in session or session['usuario'] != 'portaria':
        flash('Acesso negado. Faça login como portaria.')
        return redirect(url_for('login'))

    return render_template('dashboard_portaria.html', nome=COND_NOME, logo=COND_LOGO, cores=COND_CORES)


@app.route('/relatorios')
def relatorios():
    if 'usuario' not in session or session['usuario'] != 'sindico':
        flash('Acesso negado. Faça login como síndico para ver os relatórios.')
        return redirect(url_for('login'))

    dados = []
    with open(DADOS_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dados.append(row)

    return render_template('relatorios.html', dados=dados, nome=COND_NOME, logo=COND_LOGO, cores=COND_CORES)


@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Logout realizado com sucesso.')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

