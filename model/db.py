import sqlite3,os

class Usuario:

    def __init__(self,nome,cartao,cpf):
        self.nome = nome
        self.cartao = cartao
        self.cpf = cpf

class BancoDeDados:

    def __init__(self):
        self.conn = None
    
    def conectar_banco(self):
        #criando banco no mesmo diretorio
        path = os.path.join(os.path.dirname(__file__),'usuarios.db')
        self.conn = sqlite3.connect(path)
        return self.conn
    
    def criar_tabela(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuarios (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cartao TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                news TEXT DEFAULT 'vazio',
                data_cadastro DATE DEFAULT (date('now'))
                )
            ''')
        self.conn.commit()

    def fechar_conexao(self):
        self.conn.close()
        self.conn = None