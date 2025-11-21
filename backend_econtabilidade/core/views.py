from django.shortcuts import render

# Create your views here.

# index
def index(request):
    return render(request, 'index.html')

# cadastro
def cadastro_usuario(request):
    return render(request, 'cadastro.html')

# login 
def login_usuario(request):
    return render(request, 'login.html')

# consulta DAS cliente
def consulta_das_cliente(request):
    return render(request, 'consulta_das_cliente.html')

# consulta DAS cont
def consulta_das_cont(request):
    return render(request, 'consulta_das_cont.html')

# dashboard cliente
def dashboard_cliente(request):
    return render(request, 'dashboard_cliente.html')

# dashboard cont
def dashboard_cont(request):
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