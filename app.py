import os
import json
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "segredo"
CONFIG_PATH = 'config.json'
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    config = load_config()
    return render_template("index.html", config=config)

@app.route("/dashboard-sindico", methods=["GET", "POST"])
def dashboard_sindico():
    if session.get("tipo") != "sindico":
        return redirect("/login")

    config = load_config()

    if request.method == "POST":
        config["nome_condominio"] = request.form.get("nome_condominio")
        config["cor1"] = request.form.get("cor1")
        config["cor2"] = request.form.get("cor2")
        config["cor3"] = request.form.get("cor3")

        if 'logo' in request.files:
            file = request.files['logo']
            if file and allowed_file(file.filename):
                filename = "logo_" + file.filename
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                config["logo"] = filename

        save_config(config)

    return render_template("dashboard_sindico.html", config=config)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        tipo = request.form.get("tipo")
        if tipo in ["sindico", "portaria"]:
            session["tipo"] = tipo
            return redirect(f"/dashboard-{tipo}")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
