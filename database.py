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


if __name__ == '__main__': 
    criar_tabelas()