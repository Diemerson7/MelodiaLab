import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


def conectar_banco():
    conexao = sqlite3.connect("tarefas.db")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''create table if not exists usuarios
                   (email text primary key, nome text, senha text)''')
    
    cursor.execute('''create table if not exists projetos_musicais
                   (id integer primary key, nome_musica text, artista text, status text, letra text, caminho_capa text, email text,
                    FOREIGN KEY(email) REFERENCES usuarios(email))''')

    conexao.commit()

def criar_usuarios(formulario):
    # Ver se já existe esse email no banco de dados
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT count(email) FROM usuarios WHERE email=?''', (formulario['email'],))
    conexao.commit()
    
    quantidade_de_emails_cadastrados = cursor.fetchone()
    print(quantidade_de_emails_cadastrados)
    if (quantidade_de_emails_cadastrados[0 > 0]):
        print("LOG: Já existe esse e-mail cadastrado no banco!")
        return False
    
    senha_criptografada = generate_password_hash(formulario['senha'])
    cursor.execute('''INSERT INTO usuarios (email, nome, senha)
                    VALUES (?, ?, ?)''',
                    (formulario['email'], formulario['usuario'], senha_criptografada))
    conexao.commit() 
    return True


def fazer_login(formulario):
    # Ver se já existe esse email no banco de dados
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT count(email) FROM usuarios WHERE email=?''', (formulario['email'],))
    conexao.commit()

    quantidade_de_emails_cadastrados = cursor.fetchone()
    print(quantidade_de_emails_cadastrados)
    if (quantidade_de_emails_cadastrados[0] <= 0):
        print("LOG: Não existe esse e-mail cadastrado no banco!")
        return False
    else:
        cursor = conexao.cursor()
        cursor.execute('''SELECT senha FROM usuarios WHERE email=?''', (formulario['email'],))
        conexao.commit()
        senha_criptografada = cursor.fetchone()
        resultado_verificacao = check_password_hash(senha_criptografada[0], formulario['password'])
        return resultado_verificacao


def criar_musica(nome, artista, status, letra, caminho_capa, email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO projetos_musicais (nome_musica, artista, status, letra, caminho_capa, email) 
                   VALUES (?, ?, ?, ?, ?, ?)''', (nome, artista, status, letra, caminho_capa, email))
    conexao.commit()
    cursor.close()
    
    
def selecionar_musicas(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM projetos_musicais WHERE email=?''', (email,))
    return cursor.fetchall()

def selecionar_musica(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT id FROM projetos_musicais WHERE id=?''', (id,))
    return cursor.fetchone()


def excluir_musica(id):
    print(id)
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''DELETE FROM projetos_musicais WHERE id=?''', (id,))
    conexao.commit()
    cursor.close()

def editar_musica(nome, artista, status, letra, caminho_capa, id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''UPDATE projetos_musicais SET nome_musica=?, artista=?, status=?, letra=?, caminho_capa=? WHERE id=?''', (nome, artista, status, letra, caminho_capa, id))
    conexao.commit()
    cursor.close()
    
def deletar_usuario(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''DELETE FROM usuarios WHERE email=?''', (email,))
    cursor.execute('''DELETE FROM projetos_musicais WHERE email=?''', (email,))
    conexao.commit()
    cursor.close()
    
    











if __name__ == '__main__': 
    criar_tabelas()