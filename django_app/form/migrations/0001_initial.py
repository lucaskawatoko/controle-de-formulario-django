# Generated by Django 5.1.2 on 2024-10-30 16:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Indicacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_indicado', models.CharField(max_length=100)),
                ('email_indicado', models.EmailField(max_length=254, unique=True)),
                ('pessoa_que_indicou', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indicacoes', to='form.pessoa')),
            ],
        ),
    ]
