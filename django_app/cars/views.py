from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Car, CarImage
from django.shortcuts import render, redirect
from django.views import View
from .forms import CarForm, CarImageForm

class HomeView(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'cars/home.html'
    context_object_name = 'cars'
    login_url = 'http://127.0.0.1:8000/accounts/login/'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        user_id = self.request.GET.get('user_id')  # Pega o user_id da URL, se existir

        # Filtra os carros pelo user_id, se fornecido
        if user_id:
            queryset = queryset.filter(user__id=user_id)

        if search:
            queryset = queryset.filter(
                Q(model__name__icontains=search) |
                Q(brand__name__icontains=search)
            )

        # Filtra carros que não estão vendidos ou reservados e ordena por data de criação (mais novos primeiro)
        queryset = queryset.exclude(status__in=['sold', 'reserved']).order_by('-created_at')
        
        return queryset


class CarListView(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'cars/home.html'
    context_object_name = 'cars'
    login_url = 'http://127.0.0.1:8000/accounts/login/'  # Define a URL de login

    def get(self, request, *args, **kwargs):
        search = self.request.GET.get('search', '').strip()
        if not search:
            return redirect('cars:home')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(model__name__icontains=search) |
                Q(brand__name__icontains=search)
            )
        # Filtra carros que não estão vendidos ou reservados
        queryset = queryset.exclude(status__in=['sold', 'reserved'])
        return queryset

class CarCreateView(LoginRequiredMixin, View):
    login_url = 'http://127.0.0.1:8000/accounts/login/'

    def get(self, request):
        car_form = CarForm()
        image_form = CarImageForm()
        return render(request, 'cars/car_form.html', {'car_form': car_form, 'image_form': image_form})

    def post(self, request):
        car_form = CarForm(request.POST)
        image_form = CarImageForm(request.POST, request.FILES)

        if car_form.is_valid() and image_form.is_valid():
            car = car_form.save(commit=False)
            car.user = request.user
            car.save()

            # Salva as imagens associadas ao carro
            images = request.FILES.getlist('image')
            for img in images:
                CarImage.objects.create(car=car, image=img)

            return redirect('cars:home')

        return render(request, 'cars/car_form.html', {'car_form': car_form, 'image_form': image_form})