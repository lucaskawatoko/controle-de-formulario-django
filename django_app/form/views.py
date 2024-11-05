from django.views.generic import FormView
from django.shortcuts import redirect
from .forms import DevForm
from .models import Pessoa, Indicacao
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

class RegisterHomeView(FormView):
    template_name = 'form/register-home.html'
    form_class = DevForm
    success_url = '/register_home/'  # Redireciona para a mesma página após o sucesso

    def form_valid(self, form):
        # Obter dados do formulário
        seu_nome = form.cleaned_data['seu_nome']
        seu_email = form.cleaned_data['seu_email']
        nome_indicado = form.cleaned_data['nome_indicado']
        email_indicado = form.cleaned_data['email_indicado']

        # Verificar se o e-mail indicado já está cadastrado
        if Indicacao.objects.filter(email_indicado=email_indicado).exists():
            messages.error(self.request, 'Este email já foi indicado e não pode ser indicado novamente.')
        else:
            # Verificar se o e-mail indicado já indicou a pessoa que está indicando agora
            indicacao_inversa = Indicacao.objects.filter(email_indicado=seu_email, pessoa_que_indicou__email=email_indicado).exists()
            if indicacao_inversa:
                messages.error(self.request, 'Você não pode indicar uma pessoa que já indicou você.')
            else:
                # Obter ou criar a pessoa que está indicando
                pessoa_que_indicou, created = Pessoa.objects.get_or_create(
                    email=seu_email,
                    defaults={'nome': seu_nome}
                )

                # Criar a indicação
                nova_indicacao = Indicacao.objects.create(
                    pessoa_que_indicou=pessoa_que_indicou,
                    nome_indicado=nome_indicado,
                    email_indicado=email_indicado
                )

                # Enviar email para a pessoa que indicou
                assunto_indicador = 'Confirmação da indicação'
                mensagem_indicador = f"""
                Olá {pessoa_que_indicou.nome},

                Obrigado por indicar {nome_indicado}.

                Atenciosamente,
                Equipe de Cadastro
                """

                send_mail(
                    assunto_indicador,
                    mensagem_indicador,
                    settings.DEFAULT_FROM_EMAIL,
                    [seu_email],
                    fail_silently=False,
                )

                # Enviar email para a pessoa indicada
                assunto_indicado = 'Você foi indicado'
                mensagem_indicado = f"""
                Olá {nome_indicado},

                Você foi indicado por {pessoa_que_indicou.nome} para se cadastrar em nossa plataforma.
                Entre em contato para mais informações.

                Atenciosamente,
                Equipe de Cadastro
                """

                send_mail(
                    assunto_indicado,
                    mensagem_indicado,
                    settings.DEFAULT_FROM_EMAIL,
                    [email_indicado],
                    fail_silently=False,
                )

                messages.success(self.request, 'Indicação realizada com sucesso!')
                return redirect('form:register_home')

        # Se houver erros, retorna ao formulário
        return super().form_invalid(form)
