from django.shortcuts import render, redirect, get_object_or_404
from .admin import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .forms import EditProfileForm
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me')  # Obtém o valor do campo "Lembre-me"
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Configura a duração da sessão com base no "Lembre-me"
            if remember_me:
                request.session.set_expiry(1209600)  # 2 semanas em segundos
            else:
                request.session.set_expiry(0)  # Expira quando o navegador fecha
            
            return redirect('cars:home')  # Substitua pelo caminho correto da sua página inicial
        else:
            # Adicione uma mensagem de erro caso as credenciais sejam inválidas
            return render(request, 'accounts/login.html', {'error': 'Usuário ou senha inválidos'})
    
    return render(request, 'accounts/login.html')

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, redirect
from .models import UserProfile

class ProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'registration/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        # Obtém o perfil com base no slug da URL
        profile = get_object_or_404(UserProfile, slug=self.kwargs.get('slug'))
        
        # Verifica se o perfil pertence ao usuário autenticado
        if profile.user != self.request.user:
            # Redireciona para o perfil do próprio usuário
            return redirect('profile', slug=self.request.user.profile.slug)
        
        return profile



# Create your views here.
def register(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')  # Salva o first name
            user.last_name = form.cleaned_data.get('last_name')    # Salva o last name
            user.is_valid = False  # Ou qualquer outro campo personalizado
            user.save()
            messages.success(request, 'Registrado. Agora faça o login para começar!')
            return redirect('cars:home')
        else:
            print('invalid registration details')
            
    return render(request, "registration/register.html", {"form": form})

def custom_password_reset(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        try:
            user = User.objects.get(username=username, email=email)
            # Gera o token de redefinição de senha
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # URL para redefinir senha
            reset_url = request.build_absolute_uri(
                reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
            )

            # Envio do e-mail
            subject = "Redefinição de Senha"
            message = render_to_string("registration/password_reset_email.html", {
                "user": user,
                "reset_url": reset_url,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            messages.success(request, "Um link de redefinição de senha foi enviado para seu e-mail.")
            return redirect("login")

        except User.DoesNotExist:
            messages.error(request, "Usuário ou e-mail inválido.")

    return render(request, "registration/password_reset_form.html")

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('accounts:profile', slug=request.user.profile.slug)
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'registration/edit_profile.html', {'form': form})