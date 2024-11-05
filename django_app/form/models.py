from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Cada pessoa deve ter um email único

    def __str__(self):
        return self.nome

class Indicacao(models.Model):
    pessoa_que_indicou = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='indicacoes')
    nome_indicado = models.CharField(max_length=100)
    email_indicado = models.EmailField(unique=True)  # Email do indicado deve ser único no banco de dados

    def __str__(self):
        return f'{self.pessoa_que_indicou.nome} indicou {self.nome_indicado}'
