import pandas as pd
from model.db import Usuario, BancoDeDados
from controller.CRUD import criar_user, obter_user_por_id,salvar_mensagem_usuario
import json,os
from dotenv import load_dotenv
from openai import OpenAI

bd = BancoDeDados()

def iniciar_banco():
    bd.conectar_banco()
    bd.criar_tabela()
    bd.fechar_conexao()

#ADICIONE NOVOS USUARIOS ABAIXO

user1 = Usuario(nome="maquiavel", cartao="0001-11-2312-431", cpf="123.456.789-00")
user2 = Usuario(nome="graham", cartao="3030-30-3030-303", cpf="125.007.963-21")
user3 = Usuario(nome="sagan", cartao="2026-21-1221-502", cpf="303.003.030-30")

iniciar_banco()
criar_user(user1)
criar_user(user2)
criar_user(user3)

df = pd.read_csv('user-id.csv')
users_ids = df['UserID'].tolist()

print("IDs dos usuarios no CSV: ")
print(users_ids)

#cria um dicionario apenas com usuarios validos no banco sem repeticao
colunas = ['UserID', 'nome', 'cartao', 'cpf','news', 'data_cadastro']
users_dict = {}
for id in users_ids:
    user = obter_user_por_id(id)
    if user is not None:
        users_dict[user[0]] = dict(zip(colunas, user))
users = list(users_dict.values())

print("Usuarios validados no banco: ")
print(json.dumps(users,indent=4))

#conectando API
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key = OPENAI_API_KEY)

def gerar_mensagem_personalizada(user):

    response = client.responses.create(
        model="gpt-5-nano",
        input=f"Envie uma frase filosófica de uma ou duas linhas para o usuario {user['nome']}",
        store=True,
    )

    # valida:
    output = getattr(response, "output", None)
    if not output:
        return ""

    primeiro = output[0]
    content = primeiro.get("content") if isinstance(primeiro, dict) else None
    if not content:
        return "Sem resposta"

    fragmento = content[0]
    texto = fragmento.get("text") if isinstance(fragmento, dict) else None
    return (texto or "API sem resposta").strip()

for user in users:
    mensagem = gerar_mensagem_personalizada(user)
    print(mensagem)
    salvar_mensagem_usuario(user['UserID'], mensagem)