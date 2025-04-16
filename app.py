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
            session['email'] = form['email']    # Armazena o email do usuário na sessão
            return redirect(url_for('home')) 
        else:
            return "Ocorreu um erro ao fazer login"
    else:
        return render_template('login.html')


@app.route('/home')
def home():
    musicas = database.selecionar_musicas(session['email'])
    print(musicas)
    return render_template('home.html', musicas = musicas)


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


@app.route('/criar_musica', methods=["GET", "POST"])
def criar_musica():
    if request.method=="GET":
        return render_template('criar_musica.html')
    if request.method == "POST":
      
        nome = request.form['nome_da_musica']
        artista = request.form['artista']
        status = request.form['status']
        caminho_capa = request.form['caminho_capa'] 
        letra = request.form['letra']
        
        database.criar_musica(nome, artista, status, letra, caminho_capa, session['email'])
        musicas = database.selecionar_musicas(session['email'])
        return redirect(url_for('home'))
    
@app.route('/editar/<id>', methods=["GET", "POST"])
def editar(id):
    if request.method=="GET":
        musica = database.selecionar_musica(id)
        return render_template('editar.html', musica = musica)


@app.route('/excluir_musica/<id>')
def excluir(id):
    print(id[0])
    database.excluir_musica(id[0])
    return redirect('/home')

@app.route('/editar_musicas/<id>', methods=["POST"])
def editar_musica(id):
    if request.method == "POST":
        nome = request.form['nome']
        artista = request.form['artista']
        status = request.form['status']
        caminho_capa = request.form['caminho_capa'] 
        letra = request.form['letra']
        database.editar_musica(nome, artista, status, letra, caminho_capa, id)
        return redirect('/home')
              
@app.route('/deletar_conta')
def deletar_conta():
    database.deletar_usuario(session['email'])
    return redirect('/')



# parte principal 
if __name__ == '__main__':
    app.run(debug=True)