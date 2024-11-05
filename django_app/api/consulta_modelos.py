import requests
import json
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente
load_dotenv(dotenv_path='dotenv_files/.env')

# Seu token da API
token = os.getenv('API_TOKEN')

# Diretório atual onde o script está localizado
script_dir = os.path.dirname(os.path.abspath(__file__))

# Caminho absoluto para o arquivo JSON (ajusta isso de acordo com seu diretório)
json_file_path = os.path.join(script_dir, 'data', 'dados_marcas.json')

# Verificar se o arquivo existe
if not os.path.exists(json_file_path):
    print(f"Erro: O arquivo {json_file_path} não foi encontrado.")
    exit(1)

# Carregar o arquivo JSON com os dados das marcas
with open(json_file_path, 'r', encoding='utf-8') as f:
    marcas = json.load(f)

# Dicionário para armazenar todos os dados de modelos
modelos_data = {}

print("Iniciando o processo de consulta aos modelos das marcas...\n")

# Iterar sobre todas as chaves no arquivo JSON (por exemplo, "1", "2", "3")
for key in marcas:
    for brand_data in marcas[key]:
        brand_id = brand_data["id"]
        brand_name = brand_data["brand"]

        print(f"Consultando modelos para a marca {brand_name} (ID {brand_id})...")

        # URL da API com o ID da marca para obter os modelos
        url = f'https://api.invertexto.com/v1/fipe/models/{brand_id}?token={token}'

        # Fazendo a requisição GET
        response = requests.get(url)

        # Verificando se a requisição foi bem-sucedida
        if response.status_code == 200:
            # Convertendo a resposta em JSON
            data = response.json()

            # Adicionando os dados dos modelos ao dicionário principal
            modelos_data[brand_name] = data

            print(f"Modelos para a marca {brand_name} obtidos com sucesso.\n")
        else:
            print(f"Erro ao consultar os modelos para a marca {brand_name} (ID {brand_id}): {response.status_code}\n")

# Caminho para salvar o arquivo de modelos
output_file_path = os.path.join(script_dir, 'data', 'dados_modelos.json')

# Salvando todos os dados de modelos em um arquivo JSON
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(modelos_data, f, ensure_ascii=False, indent=4)

print(f"Processo concluído. Todos os dados foram salvos com sucesso em '{output_file_path}'.")
