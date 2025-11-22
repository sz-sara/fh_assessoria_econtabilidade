from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib import messages

# Create your views here.

# index
def index(request):
    return render(request, 'index.html')

# cadastro
def cadastro_usuario(request):
    return render(request, 'cadastro.html')

# login 
def login_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # tenta achar o usuário
        try:
            usuario = Usuario.objects.get(email=email, senha=senha)
        except Usuario.DoesNotExist:
            messages.error(request, 'E-mail ou senha inválidos.')
            return render(request, 'login.html')

        # guarda dados básicos na sessão
        request.session['usuario_id'] = usuario.id
        request.session['tipo_de_usuario'] = usuario.tipo_de_usuario

        # redireciona conforme o tipo
        if usuario.tipo_de_usuario == 'cliente':
            return redirect('dashboard_cliente')
        elif usuario.tipo_de_usuario in ['contador']:
            return redirect('dashboard_cont')
        else:
            # se vier algum tipo inesperado, manda pra home
            return redirect('index')

    # se for GET só mostra o template
    return render(request, 'login.html')



# consulta DAS cliente
def consulta_das_cliente(request):
    return render(request, 'consulta_das_cliente.html')

# consulta DAS cont
def consulta_das_cont(request):
    return render(request, 'consulta_das_cont.html')

# dashboard cliente
def dashboard_cliente(request):
    if request.session.get('tipo_de_usuario') != 'cliente':
        return redirect('login')

    return render(request, 'dashboard_cliente.html')

# dashboard cont
def dashboard_cont(request):
    if request.session.get('tipo_de_usuario') not in ['contador', 'empresario']:
        return redirect('login')

    return render(request, 'dashboard_cont.html')

# DASMEI cliente
def DASMEI_cliente(request):
    return render(request, 'DASMEI_cliente.html')

# DASMEI cont
def DASMEI_cont(request):   
    return render(request, 'DASMEI_cont.html')

# gestão clientes cont
def gestao_clientes_cont(request):
    return render(request, 'gestao_clientes_cont.html')

# gestão impostos cont
def gestao_impostos_cont(request):  
    return render(request, 'gestao_impostos_cont.html')

# gestão tarefas cont
def gestao_tarefas_cont(request):
    return render(request, 'gestao_tarefas_cont.html')

# gestão docs
def gestaodocs(request):
    return render(request, 'gestaodocs.html')

# notificaoes cliente
def notificacoes_cliente(request):
    return render(request, 'notificacoes_cliente.html')

# notificacoes cont
def notificacoes_cont(request):
    return render(request, 'notificacoes_cont.html')

# redefinição
def redefinicao(request):
    return render(request, 'redefinicao.html')

# usuário
def usuario(request):
    return render(request, 'usuario.html')