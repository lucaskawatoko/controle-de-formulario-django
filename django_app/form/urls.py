from django.urls import path
from . import views

app_name = 'form'

urlpatterns = [
    path('register-home/', views.RegisterHomeView.as_view(), name='register_home'),
]
