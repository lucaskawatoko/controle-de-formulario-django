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

from cars.models import Brand, Model  # Certifique-se de ajustar o nome da app se necessário

# Caminho para o arquivo JSON de modelos
json_file = os.path.join(script_dir, './data/dados_modelos.json')

print("Iniciando o processo de cadastro dos modelos a partir do JSON...\n")

# Ler o arquivo JSON
try:
    with open(json_file, 'r', encoding='utf-8') as f:
        all_data = json.load(f)
except FileNotFoundError:
    print(f"Arquivo '{json_file}' não encontrado.")
    exit()

# Iterar sobre cada marca e seus modelos no JSON
for brand_name, models_list in all_data.items():
    # Verificar se a marca já está cadastrada no banco de dados
    brands = Brand.objects.filter(name=brand_name)
    
    if brands.count() == 0:
        print(f"Marca '{brand_name}' não encontrada no banco de dados. Pulando modelos dessa marca.")
        continue
    elif brands.count() > 1:
        print(f"⚠️ Atenção: Encontradas múltiplas marcas com o nome '{brand_name}'. Usando a primeira ocorrência.")

    brand = brands.first()

    # Iterar sobre os modelos dessa marca
    for model_data in models_list:
        model_name = model_data.get('model')

        # Verificar se os dados essenciais estão presentes
        if not model_name:
            print(f"Dados incompletos para o modelo '{model_name}' da marca '{brand_name}'. Pulando...")
            continue

        # Criar ou atualizar o modelo no banco de dados
        model, created = Model.objects.update_or_create(
            name=model_name,
            brand=brand,  # Associar corretamente com a marca encontrada
            defaults={
                'name': model_name,
                'created_at': django.utils.timezone.now(),
                'updated_at': django.utils.timezone.now()
            }
        )

        if created:
            print(f"Modelo '{model_name}' da marca '{brand_name}' cadastrado com sucesso.")
        else:
            print(f"Modelo '{model_name}' da marca '{brand_name}' já existe. Dados atualizados.")

print("\nProcesso de cadastro dos modelos concluído.")
