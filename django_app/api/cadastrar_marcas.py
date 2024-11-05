import sys
import os
import django
import json

# Obter o diretório atual do script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Obter o diretório raiz do projeto (um nível acima)
project_root = os.path.abspath(os.path.join(script_dir, '..'))

# Adicionar o diretório raiz do projeto ao sys.path
sys.path.append(project_root)

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  # Substitua 'project' pelo nome do seu projeto
django.setup()

from cars.models import Brand  # Substitua 'sua_app' pelo nome da sua aplicação

# Caminho para o arquivo JSON
json_file = os.path.join(script_dir, './data/dados_marcas.json')

print("Iniciando o processo de cadastro das marcas a partir do JSON...\n")

# Ler o arquivo JSON
try:
    with open(json_file, 'r', encoding='utf-8') as f:
        all_data = json.load(f)
except FileNotFoundError:
    print(f"Arquivo '{json_file}' não encontrado.")
    exit()

# Iterar sobre os tipos de veículo e suas marcas
for vehicle_type_str, brands_list in all_data.items():
    # Converter o tipo de veículo para inteiro
    vehicle_type = int(vehicle_type_str)
    
    for brand_data in brands_list:
        if 'brand' in brand_data:
            brand_name = brand_data['brand']
            
            # Criar ou atualizar a marca no banco de dados
            brand, created = Brand.objects.update_or_create(
                name=brand_name,
                vehicle_type=vehicle_type,
                defaults={'name': brand_name, 'vehicle_type': vehicle_type}
            )
            
            if created:
                print(f"Marca '{brand_name}' (Tipo {vehicle_type}) cadastrada com sucesso.")
            else:
                print(f"Marca '{brand_name}' (Tipo {vehicle_type}) já existe. Dados atualizados.")
        else:
            print(f"Dados da marca não contêm o campo 'brand'.\n")

print("\nProcesso concluído.")
