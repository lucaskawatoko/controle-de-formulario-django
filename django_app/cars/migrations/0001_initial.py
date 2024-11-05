# Generated by Django 5.1.2 on 2024-10-30 16:49

import cars.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('vehicle_type', models.IntegerField(choices=[(1, 'Carro'), (2, 'Moto'), (3, 'Caminhão')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factory_year', models.IntegerField()),
                ('model_year', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('mileage', models.PositiveIntegerField(default=0)),
                ('color', models.CharField(blank=True, max_length=50, null=True)),
                ('fuel_type', models.CharField(blank=True, choices=[('gasoline', 'Gasolina'), ('diesel', 'Diesel'), ('ethanol', 'Etanol'), ('hybrid', 'Híbrido'), ('electric', 'Elétrico')], max_length=10, null=True)),
                ('transmission', models.CharField(blank=True, choices=[('manual', 'Manual'), ('automatic', 'Automático')], max_length=10, null=True)),
                ('traction', models.CharField(blank=True, choices=[('fwd', 'Tração Dianteira'), ('rwd', 'Tração Traseira'), ('awd', 'Tração Integral'), ('4wd', 'Tração nas Quatro Rodas')], max_length=10, null=True)),
                ('status', models.CharField(choices=[('available', 'Disponível'), ('sold', 'Vendido'), ('reserved', 'Reservado')], default='available', max_length=10)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.brand')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CarImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='cars/%Y/%m/%d/', validators=[cars.models.validate_image_extension])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='cars.car')),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.brand')),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.model'),
        ),
    ]
