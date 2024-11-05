import openpyxl
from django.http import HttpResponse
from django.contrib import admin
from .models import Pessoa, Indicacao
from django.urls import path
from django.template.response import TemplateResponse

# Função de exportação para o model Pessoa
def exportar_pessoa_para_excel(modeladmin, request, queryset):
    # Cria um workbook e uma planilha
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pessoas"

    # Adiciona cabeçalhos na primeira linha
    ws.append(['Nome', 'Email'])

    # Adiciona os dados do queryset
    for pessoa in queryset:
        ws.append([pessoa.nome, pessoa.email])

    # Prepara a resposta HTTP para o download
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=pessoas.xlsx'

    # Salva o workbook na resposta
    wb.save(response)

    return response

exportar_pessoa_para_excel.short_description = "Exportar selecionados para Excel"

# Função de exportação para o model Indicacao
def exportar_indicacao_para_excel(modeladmin, request, queryset):
    # Cria um workbook e uma planilha
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Indicações"

    # Adiciona cabeçalhos na primeira linha (com email da pessoa que indicou)
    ws.append(['Pessoa que Indicou', 'Email da Pessoa que Indicou', 'Nome Indicado', 'Email Indicado'])

    # Adiciona os dados do queryset
    for indicacao in queryset:
        ws.append([indicacao.pessoa_que_indicou.nome, indicacao.pessoa_que_indicou.email,
                   indicacao.nome_indicado, indicacao.email_indicado])

    # Prepara a resposta HTTP para o download
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=indicacoes.xlsx'

    # Salva o workbook na resposta
    wb.save(response)

    return response

exportar_indicacao_para_excel.short_description = "Exportar selecionados para Excel"

# Função para exibir página de download
def baixar_arquivo_indicacoes(request):
    return TemplateResponse(request, 'admin/download_indicacoes.html')

# Admin para model Pessoa
@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email')
    actions = [exportar_pessoa_para_excel]

# Admin para model Indicacao
@admin.register(Indicacao)
class IndicacaoAdmin(admin.ModelAdmin):
    list_display = ('pessoa_que_indicou', 'nome_indicado', 'email_indicado')
    actions = [exportar_indicacao_para_excel]
    list_filter = ('pessoa_que_indicou',)  # Filtro por pessoa que indicou

    # Adicionando URL para página de download
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('baixar-indicacoes/', baixar_arquivo_indicacoes, name='baixar_indicacoes'),
        ]
        return custom_urls + urls
