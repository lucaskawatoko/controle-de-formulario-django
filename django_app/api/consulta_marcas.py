import requests
import json
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='dotenv_files/.env')

# Lista de IDs de marcas para iterar (por exemplo, de 1 a 10)
brand_ids = range(1, 11)  # Você pode ajustar o intervalo conforme necessário

# Seu token da API
token = os.getenv('API_TOKEN')

# Dicionário para armazenar todos os dados
all_data = {}

print("Iniciando o processo de consulta às marcas...\n")

for brand_id in brand_ids:
    # URL da API com o ID da marca
    url = f'https://api.invertexto.com/v1/fipe/brands/{brand_id}?token={token}'
    
    print(f"Consultando dados para a marca ID {brand_id}...")
    
    # Fazendo a requisição GET
    response = requests.get(url)
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Convertendo a resposta em JSON
        data = response.json()
        
        # Adicionando os dados ao dicionário principal
        all_data[brand_id] = data
        
        print(f"Dados para a marca ID {brand_id} obtidos com sucesso.\n")
    else:
        print(f"Erro ao consultar a marca ID {brand_id}: {response.status_code}\n")

# Salvando todos os dados em um arquivo JSON
with open('./data/dados_marcas.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print("Processo concluído.")
print("Todos os dados foram salvos com sucesso em 'dados_marcas.json'")
