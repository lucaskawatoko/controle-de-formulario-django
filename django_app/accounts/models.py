import hashlib
import uuid
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

# Modelo UserProfile para estender informações do usuário
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    slug = models.CharField(max_length=64, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Gera um UUID e aplica o SHA-256 para aumentar a segurança do slug
            uuid_value = uuid.uuid4().hex
            hash_object = hashlib.sha256(uuid_value.encode())
            self.slug = hash_object.hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Perfil de {self.user.username}"

# Modelo CustomUser para substituir o modelo User padrão do Django
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)  # Novo campo de telefone

    def save(self, *args, **kwargs):
        # Remove espaços extras do username e permite espaços no meio
        self.username = " ".join(self.username.split())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


# Sinais para criar e salvar automaticamente o UserProfile ao criar um CustomUser
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()