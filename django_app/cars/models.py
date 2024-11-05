import os
from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import sys
import shutil 

# Função para validar extensão da imagem
def validate_image_extension(value):
    valid_extensions = ['jpg', 'jpeg', 'png']  # Apenas JPG, JPEG e PNG permitidos
    ext = value.name.split('.')[-1].lower()  # Extrai a extensão do arquivo
    if ext not in valid_extensions:
        raise ValidationError('Tipo de arquivo não suportado. Use apenas jpg, jpeg ou png.')

# Função para compressão e redimensionamento de imagens
def compress_image(image, ext):
    img = Image.open(image)
    output_io_stream = BytesIO()

    # Compressão baseada no tipo de imagem
    if ext in ['jpg', 'jpeg']:
        img = img.convert("RGB")  # Converte para JPEG (não suporta transparência)
        img.save(output_io_stream, format='JPEG', quality=70)  # Compressão JPEG
    elif ext == 'png':
        img.save(output_io_stream, format='PNG', quality=70)  # Compressão PNG

    output_io_stream.seek(0)
    return InMemoryUploadedFile(output_io_stream, 'ImageField', "%s.%s" % (image.name.split('.')[0], ext), 'image/%s' % ext, sys.getsizeof(output_io_stream), None)

# Modelo de Marca
class Brand(models.Model):
    VEHICLE_TYPE_CHOICES = (
        (1, 'Carro'),
        (2, 'Moto'),
        (3, 'Caminhão'),
    )
    name = models.CharField(max_length=100)
    vehicle_type = models.IntegerField(choices=VEHICLE_TYPE_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_vehicle_type_display()})"

# Modelo de Carro
class Model(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class Car(models.Model):
    FUEL_CHOICES = [
        ('gasoline', 'Gasolina'),
        ('diesel', 'Diesel'),
        ('ethanol', 'Etanol'),
        ('hybrid', 'Híbrido'),
        ('electric', 'Elétrico'),
    ]

    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automático'),
    ]

    TRACTION_CHOICES = [
        ('fwd', 'Tração Dianteira'),
        ('rwd', 'Tração Traseira'),
        ('awd', 'Tração Integral'),
        ('4wd', 'Tração nas Quatro Rodas'),
    ]

    STATUS_CHOICES = [
        ('available', 'Disponível'),
        ('sold', 'Vendido'),
        ('reserved', 'Reservado'),
    ]

    model = models.ForeignKey('Model', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    factory_year = models.IntegerField()
    model_year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)  # Valor sem centavos
    mileage = models.PositiveIntegerField(default=0)  # Quilometragem
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cars')
    color = models.CharField(max_length=50, blank=True, null=True)  # Cor
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES, blank=True, null=True)  # Tipo de combustível
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES, null=True, blank=True)  # Tipo de câmbio
    traction = models.CharField(max_length=10, choices=TRACTION_CHOICES, null=True, blank=True)  # Tipo de tração
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')  # Status do carro
    description = models.TextField(blank=True)  # Descrição opcional
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.brand} {self.model} ({self.model_year})'

# Modelo para armazenar múltiplas imagens de cada carro
class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cars/%Y/%m/%d/', validators=[validate_image_extension])
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.image:
            ext = self.image.name.split('.')[-1].lower()
            self.image = compress_image(self.image, ext)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.car}"

# Sinal para deletar a imagem associada ao carro quando o registro for excluído
@receiver(post_delete, sender=CarImage)
def delete_car_image(sender, instance, **kwargs):
    """
    Deleta a imagem associada ao CarImage quando o registro é excluído.
    """
    if instance.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))
        if os.path.isfile(image_path):
            os.remove(image_path)

# Sinal para deletar a imagem antiga quando uma nova é enviada
@receiver(post_delete, sender=CarImage)
def delete_car_image(sender, instance, **kwargs):
    """
    Deleta a imagem associada ao CarImage quando o registro é excluído.
    Se a pasta do dia ficar vazia, também a remove.
    Se a pasta do mês ficar vazia após remoção de dias, também a remove.
    """
    if instance.image:
        # Caminho completo da imagem
        image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))
        if os.path.isfile(image_path):
            os.remove(image_path)  # Exclui a imagem
        day_dir = os.path.dirname(image_path)
        month_dir = os.path.dirname(day_dir)

        if not os.listdir(day_dir): 
            shutil.rmtree(day_dir)
            if not os.listdir(month_dir): 
                shutil.rmtree(month_dir)