# forms.py
from django import forms
from .models import Car, CarImage

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'model', 'brand', 'factory_year', 'model_year', 'price', 
            'mileage', 'color', 'fuel_type', 'transmission', 'traction', 
            'status', 'description'
        ]

class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ['image']
