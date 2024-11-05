from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile
from .forms import CustomUserCreationForm

# Customização do Django Admin para UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug')  # Exibe o nome do usuário e o slug na lista

admin.site.register(UserProfile, UserProfileAdmin)

# Customização do Django Admin para CustomUser
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser

    # Campos a serem exibidos na visualização de detalhes do usuário
    fieldsets = (
        ('Informações Pessoais', {'fields': ('username', 'email', 'first_name', 'last_name', 'telefone')}),  # Adicionado 'telefone' aqui
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Campos ao adicionar um novo usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'telefone', 'password1', 'password2'),  # Adicionado 'telefone' aqui
        }),
    )

    # Campos a serem exibidos na lista de usuários
    list_display = ('username', 'email', 'first_name', 'last_name', 'telefone', 'is_staff')  # Adicionado 'telefone' aqui

admin.site.register(CustomUser, CustomUserAdmin)
