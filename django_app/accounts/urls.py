from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/<slug:slug>/', views.ProfileView.as_view(), name='profile'),
    path("reset_password/", views.custom_password_reset, name="custom_password_reset"),
    path('editar-perfil/', views.edit_profile, name='edit_profile'),
]