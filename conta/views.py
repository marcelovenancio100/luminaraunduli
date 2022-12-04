from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato


def login(request):
    if request.method != 'POST':
        return render(request, 'conta/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválida!')
        return render(request, 'conta/login.html')
    else:
        auth.login(request, user)
        messages.success(request, f'Você está logado como {usuario}')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    if request.method != 'POST':
        return render(request, 'conta/register.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    redsenha = request.POST.get('redsenha')

    if not nome or not sobrenome or not email or not usuario or not senha or not redsenha:
        messages.error(request, 'Necessário informar todos os campos!')
        return render(request, 'conta/register.html')

    try:
        validate_email(email)
    except Exception as e:
        messages.error(request, 'Email inválido!')
        return render(request, 'conta/register.html')

    if len(usuario) < 6:
        messages.error(request, 'Usuário precisa ter no mínimo 6 caracteres!')
        return render(request, 'conta/register.html')

    if len(senha) < 6:
        messages.error(request, 'Senha precisa ter no mínimo 6 caracteres!')
        return render(request, 'conta/register.html')

    if senha != redsenha:
        messages.error(request, 'As senhas precisam ser iguais!')
        return render(request, 'conta/register.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, f'Já existe um usuário com o nome {usuario}')
        return render(request, 'conta/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, f'Já existe um usuário com o email {email}')
        return render(request, 'conta/register.html')

    print(request.POST)

    user = User.objects.create_user(username=usuario, email=email, first_name=nome, last_name=sobrenome, password=senha)
    user.save()
    messages.success(request, 'Conta criada com sucesso!')
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form_contato = FormContato()
        return render(request, 'conta/dashboard.html', {'form_contato': form_contato})

    form_contato = FormContato(request.POST, request.FILES)

    if not form_contato.is_valid():
        messages.error(request, 'Erro ao cadastrar contato!')
        form_contato = FormContato(request.POST)
        return render(request, 'conta/dashboard.html', {'form_contato': form_contato})

    form_contato.save()
    messages.success(request, f'Contato {request.POST.get("nome")} salvo com sucesso!')
    return redirect('dashboard')
