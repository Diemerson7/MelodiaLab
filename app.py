from flask import Flask, render_template, request, session, url_for, redirect, flash

import database

app = Flask(__name__)
app.secret_key = "chave_muito_segura"


@app.route('/') #rota para a página inicial
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"]) #rota para a página de login
def login():
    if request.method == "POST":
        form = request.form
        if database.fazer_login(form) == True:
            session['usuario'] = form['email']    # Armazena o email do usuário na sessão
            return redirect(url_for('home')) 
        else:
            return "Ocorreu um erro ao fazer login"
    else:
        return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/cadastro', methods=["GET", "POST"]) #rota para a página de login
def cadastro():
    if request.method == "POST":
        form = request.form
        
        if database.criar_usuarios(form) == True:
            return render_template ('login.html')
        else:
            return "Ocorreu um erro ao cadastrar o usuário"
    else:
            return render_template('cadastro.html')


# parte principal do
if __name__ == '__main__':
    app.run(debug=True)