import sqlite3
from model.db import BancoDeDados

bd = BancoDeDados()

#Colunas
valid_cols = ['UserID', 'nome', 'cartao', 'cpf']

def proteger_sql_injection(col):
    if col not in valid_cols:
        raise ValueError("Coluna inválida")
    return f'SELECT * FROM Usuarios WHERE {col} = ?'
    
def criar_user(dados):
    conn = bd.conectar_banco()
    cursor = conn.cursor()
    
    try:
            cursor.execute('''
                INSERT INTO Usuarios (nome, cartao, cpf)
                VALUES (?, ?, ?)
            ''', (dados.nome, dados.cartao, dados.cpf))
            conn.commit()
            
            return True
    except sqlite3.IntegrityError:
            print("Erro: CPF já cadastrado!")
            return None
    finally:
            bd.fechar_conexao()

def obter_users():
 conn = bd.conectar_banco()
 cursor = conn.cursor()
 cursor.execute('SELECT * FROM Usuarios')

 #transforma tupla do banco para dicionario
 colunas = [desc[0] for desc in cursor.description]
 membros = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
 
 bd.fechar_conexao()
 return membros

def obter_user_por_id(id_user):
 conn = bd.conectar_banco()
 cursor = conn.cursor()

 query = proteger_sql_injection('UserID')
 cursor.execute(query, (id_user,))
 membro = cursor.fetchone()
 bd.fechar_conexao()
 return membro

def salvar_mensagem_usuario(user_id, news):
    conn = bd.conectar_banco()
    cursor = conn.cursor()
    cursor.execute("UPDATE Usuarios SET news = ? WHERE UserID = ?", (news, user_id))
    conn.commit()
    bd.fechar_conexao()