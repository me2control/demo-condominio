from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        placa = request.form["placa"]
        apartamento = request.form["apartamento"]
        vaga = request.form["vaga"]
        print(f"Novo visitante: {nome}, CPF: {cpf}, Placa: {placa}, Ap: {apartamento}, Vaga: {vaga}")
        return redirect(url_for("obrigado"))
    return render_template("formulario.html")

@app.route("/obrigado")
def obrigado():
    return render_template("obrigado.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
