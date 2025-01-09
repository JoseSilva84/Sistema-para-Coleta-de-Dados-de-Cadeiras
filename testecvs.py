import pandas as pd

# Ler o arquivo
df = pd.read_csv('LISTA ENROLADORES.txt', delimiter=' ', names=['Data', 'Nome', 'Objeto', 'Qt', 'V.un', 'Total'], encoding="ISO-8859-1")

# Remover colchetes e espaços de todas as colunas que têm colchetes
df['Nome'] = df['Nome'].str.replace(r'[\[\]]', '', regex=True).str.strip()
df['Total'] = df['Total'].str.replace(r'[\[\]]', '', regex=True).str.strip()

# Converter 'Total' para float
df['Total'] = pd.to_numeric(df['Total'], errors='coerce')

# Padronizar o nome pesquisado
nome_pesquisado = input('Digite o nome: ').strip().lower()

# Padronizar coluna 'Nome' para evitar problemas de capitalização
df['Nome'] = df['Nome'].str.lower()

# Filtrar e somar os valores
nome_todos = df[df['Nome'] == nome_pesquisado]
valor = nome_todos['Total'].sum()

# Mostrar o resultado
print(f'Total para {nome_pesquisado.capitalize()}: {valor}')
