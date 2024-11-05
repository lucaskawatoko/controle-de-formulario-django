from django import forms
import re

class DevForm(forms.Form):
    # Campos de cadastro
    seu_nome = forms.CharField(
        label='Seu nome', 
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    seu_email = forms.EmailField(
        label='Seu email', 
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    # Campos de indicação
    nome_indicado = forms.CharField(
        label='Nome de quem você vai indicar', 
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email_indicado = forms.EmailField(
        label='Email de quem você vai indicar', 
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    def clean_seu_email(self):
        email = self.cleaned_data.get('seu_email')
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(regex, email):
            raise forms.ValidationError("O email fornecido não parece ser válido.")
        return email

    def clean_email_indicado(self):
        email = self.cleaned_data.get('email_indicado')
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(regex, email):
            raise forms.ValidationError("O email fornecido não parece ser válido.")
        return email
