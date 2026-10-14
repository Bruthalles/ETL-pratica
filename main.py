import pandas as pd
from model.db import Usuario, BancoDeDados
from controller.CRUD import criar_user, obter_user_por_id,salvar_mensagem_usuario
import json,os
from dotenv import load_dotenv
from openai import OpenAI

banco_dados = BancoDeDados()

def iniciar_banco():
    banco_dados.conectar_banco()
    banco_dados.criar_tabela()
    banco_dados.fechar_conexao()

#ADICIONE NOVOS USUARIOS ABAIXO

user1 = Usuario(nome="maquiavel", cartao="0001-11-2312-431", cpf="123.456.789-00")
user2 = Usuario(nome="graham", cartao="3030-30-3030-303", cpf="125.007.963-21")
user3 = Usuario(nome="sagan", cartao="2026-21-1221-502", cpf="303.003.030-30")

iniciar_banco()
criar_user(user1)
criar_user(user2)
criar_user(user3)

df_usuarios = pd.read_csv('user-id.csv')
ids_usuarios = df_usuarios['UserID'].tolist()

print("IDs dos usuarios no CSV: ")
print(ids_usuarios)

#cria um dicionario apenas com usuarios validos no banco sem repeticao
colunas = ['UserID', 'nome', 'cartao', 'cpf','news', 'data_cadastro']
usuarios_por_id = {}
for id in ids_usuarios:
    user = obter_user_por_id(id)
    if user is not None:
        usuarios_por_id[user[0]] = dict(zip(colunas, user))

usuarios_validos = list(usuarios_por_id.values())

print("Usuarios validados no banco: ")
print(json.dumps(usuarios_validos,indent=4))

#conectando API
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key = OPENAI_API_KEY)

def gerar_mensagem_personalizada(user):

    resposta_api = client.responses.create(
        model="gpt-5-nano",
        input=f"Envie uma frase filosófica de uma ou duas linhas para o usuario {user['nome']}",
        store=True,
    )
    # salva somente a mensagem da resposta da API 
    mensagem_gerada = resposta_api.output_text
    
    if not mensagem_gerada:
        return "API Sem Resposta"

    return mensagem_gerada.strip()

for user in usuarios_validos:
    mensagem = gerar_mensagem_personalizada(user)
    print(mensagem)
    salvar_mensagem_usuario(user['UserID'], mensagem)