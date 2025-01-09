import os
import pandas as pd
from pandasai import Agent


#Minha chave é: $2a$10$02SCUtQBuC/nfOLLl.xs.Oj0e6F6vFJSnMwSaYTxLnO9kvf65dcIO
df = pd.read_csv("LISTA ENROLADORES.txt", delimiter=' ', header=None, names=[
            'Data', 'Enrolador', 'Objeto', 'Quantidade', 'Valor unitário', 'Valor Total'], encoding='latin1', on_bad_lines='skip')

os.environ["PANDASAI_API_KEY"] = "$2a$10$02SCUtQBuC/nfOLLl.xs.Oj0e6F6vFJSnMwSaYTxLnO9kvf65dcIO"

#print(df)
pergunta = input("pergunta: ")

agent = Agent(df)
# resposta = agent.chat("São quantos enroladores?")
resposta = agent.chat(pergunta)

print("Resposta:", resposta)