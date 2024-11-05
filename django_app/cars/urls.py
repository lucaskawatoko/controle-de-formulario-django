# cars/urls.py

from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('list/', views.CarListView.as_view(), name='list'),
]
