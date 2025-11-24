from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Empresa, EmpresasUsuarioCliente, Tarefa
from django.contrib import messages
from django.db import transaction, IntegrityError
from datetime import date

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

#excluir cliente
@transaction.atomic
def excluir_cliente(request, cnpj):
    empresa = get_object_or_404(Empresa, cnpj=cnpj)

    # pega vínculos
    relacoes = (
        EmpresasUsuarioCliente.objects
        .select_related('usuario_cliente')
        .filter(empresa_cnpj=empresa)
    )

    if request.method == 'POST':
        # guarda os usuários antes de excluir vínculos
        usuarios = [rel.usuario_cliente for rel in relacoes]

        # remove vínculos
        EmpresasUsuarioCliente.objects.filter(empresa_cnpj=empresa).delete()

        # remove empresa
        empresa.delete()

        # remove usuário sem empresas vinculadas
        for u in usuarios:
            if not u.empresas_como_cliente.exists():
                u.delete()

        messages.success(request, 'Cliente excluído com sucesso.')
        return redirect('gestao_clientes_cont')

    # GET → exibir página de confirmação
    return render(request, 'confirmar_exclusao_cliente.html', {
        'empresa': empresa,
        'relacoes': relacoes,
    })

#logout
def logout_usuario(request):
    request.session.flush()  # limpa sessão
    messages.success(request, 'Você saiu do sistema.')
    return redirect('login')
    


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
    if request.session.get('tipo_de_usuario') not in ['contador', 'cliente']:
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
    if request.method == 'POST':
        # ---------- DADOS DA EMPRESA ----------
        cnpj = request.POST.get('cnpj')
        razao_social = request.POST.get('razao_social')
        nome_fantasia = request.POST.get('nome_fantasia')
        inscricao_municipal = request.POST.get('inscricao_municipal')
        tipo_empresa = request.POST.get('tipo_empresa')

        empresa_email = request.POST.get('empresa_email')
        empresa_telefone = request.POST.get('empresa_telefone')
        empresa_logradouro = request.POST.get('empresa_logradouro')
        empresa_bairro = request.POST.get('empresa_bairro')
        empresa_cidade = request.POST.get('empresa_cidade')
        empresa_estado = request.POST.get('empresa_estado')
        empresa_cep = request.POST.get('empresa_cep')
        empresa_pais = request.POST.get('empresa_pais')
        empresa_data_registro_raw = request.POST.get('empresa_data_registro')

        # converte datas (ou deixa None)
        empresa_data_registro = None
        if empresa_data_registro_raw:
            try:
                empresa_data_registro = date.fromisoformat(empresa_data_registro_raw)
            except ValueError:
                empresa_data_registro = None

        # ---------- DADOS DO USUÁRIO (CLIENTE) ----------
        cpf = request.POST.get('cpf')
        nome = request.POST.get('nome')
        username = request.POST.get('username') or request.POST.get('email')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario_logradouro = request.POST.get('usuario_logradouro')
        usuario_bairro = request.POST.get('usuario_bairro')
        usuario_cidade = request.POST.get('usuario_cidade')
        usuario_estado = request.POST.get('usuario_estado')
        usuario_cep = request.POST.get('usuario_cep')
        usuario_pais = request.POST.get('usuario_pais')
        usuario_data_registro_raw = request.POST.get('usuario_data_registro')

        usuario_data_registro = None
        if usuario_data_registro_raw:
            try:
                usuario_data_registro = date.fromisoformat(usuario_data_registro_raw)
            except ValueError:
                usuario_data_registro = None

        try:
            with transaction.atomic():
                # --------- Empresa ---------
                empresa, _ = Empresa.objects.get_or_create(
                    cnpj=cnpj,
                    defaults={
                        'razao_social': razao_social,
                        'nome_fantasia': nome_fantasia,
                        'inscricao_municipal': inscricao_municipal,
                        'tipo_empresa': tipo_empresa,
                        'email': empresa_email,
                        'telefone': empresa_telefone,
                        'logradouro': empresa_logradouro,
                        'bairro': empresa_bairro,
                        'cidade': empresa_cidade,
                        'estado': empresa_estado,
                        'cep': empresa_cep,
                        'pais': empresa_pais,
                        'data_de_registro': empresa_data_registro or date.today(),
                    }
                )

                # Atualiza se já existia
                empresa.razao_social = razao_social
                empresa.nome_fantasia = nome_fantasia
                empresa.inscricao_municipal = inscricao_municipal
                empresa.tipo_empresa = tipo_empresa
                empresa.email = empresa_email
                empresa.telefone = empresa_telefone
                empresa.logradouro = empresa_logradouro
                empresa.bairro = empresa_bairro
                empresa.cidade = empresa_cidade
                empresa.estado = empresa_estado
                empresa.cep = empresa_cep
                empresa.pais = empresa_pais
                if empresa_data_registro:
                    empresa.data_de_registro = empresa_data_registro
                elif not empresa.data_de_registro:
                    empresa.data_de_registro = date.today()
                empresa.save()

                # --------- Usuário cliente ---------
                usuario, _ = Usuario.objects.get_or_create(
                    cpf=cpf,
                    defaults={
                        'tipo_de_usuario': 'cliente',
                        'nome': nome,
                        'username': username,
                        'email': email,
                        'telefone': telefone,
                        'senha': senha,
                        'logradouro': usuario_logradouro,
                        'bairro': usuario_bairro,
                        'cidade': usuario_cidade,
                        'estado': usuario_estado,
                        'cep': usuario_cep,
                        'pais': usuario_pais,
                        'data_de_registro': usuario_data_registro or date.today(),
                    }
                )

                usuario.tipo_de_usuario = 'cliente'
                usuario.nome = nome
                usuario.username = username
                usuario.email = email
                usuario.telefone = telefone
                usuario.senha = senha
                usuario.logradouro = usuario_logradouro
                usuario.bairro = usuario_bairro
                usuario.cidade = usuario_cidade
                usuario.estado = usuario_estado
                usuario.cep = usuario_cep
                usuario.pais = usuario_pais
                if usuario_data_registro:
                    usuario.data_de_registro = usuario_data_registro
                elif not usuario.data_de_registro:
                    usuario.data_de_registro = date.today()
                usuario.save()

                # --------- Vínculo Empresa x Usuário ---------
                EmpresasUsuarioCliente.objects.get_or_create(
                    empresa_cnpj=empresa,
                    usuario_cliente=usuario,
                    defaults={'tipo_usuario': 'cliente'}
                )

            messages.success(request, 'Cliente cadastrado com sucesso.')
        except IntegrityError:
            messages.error(
                request,
                'Erro ao cadastrar cliente. Verifique se CPF e CNPJ já não estão cadastrados.'
            )

        return redirect('gestao_clientes_cont')
    

    # GET – lista tudo
    relacoes = (
        EmpresasUsuarioCliente.objects
        .select_related('empresa_cnpj', 'usuario_cliente')
        .all()
    )
    return render(request, 'gestao_clientes_cont.html', {'relacoes': relacoes})

#detalhe dos clientes

def detalhe_cliente(request, cnpj):
    # garante que só contador/empresário veja
    if request.session.get('tipo_de_usuario') not in ['contador', 'cliente']:
        return redirect('login')

    empresa = get_object_or_404(Empresa, cnpj=cnpj)

    # todos os usuários vinculados a essa empresa
    relacoes = (
        EmpresasUsuarioCliente.objects
        .select_related('usuario_cliente')
        .filter(empresa_cnpj=empresa)
    )

    return render(
        request,
        'detalhe_cliente.html',
        {
            'empresa': empresa,
            'relacoes': relacoes,
        }
    )

#editar cliente
def editar_cliente(request, cnpj):
    empresa = get_object_or_404(Empresa, cnpj=cnpj)

    # pega todos os vínculos para listar usuários
    relacoes = (
        EmpresasUsuarioCliente.objects
        .select_related('usuario_cliente')
        .filter(empresa_cnpj=empresa)
    )

    # por enquanto, só 1 usuário principal
    usuario = relacoes[0].usuario_cliente if relacoes else None

    if request.method == 'POST':

        # --------------------- EMPRESA ---------------------
        empresa.razao_social = request.POST.get('razao_social')
        empresa.nome_fantasia = request.POST.get('nome_fantasia')
        empresa.inscricao_municipal = request.POST.get('inscricao_municipal')
        empresa.tipo_empresa = request.POST.get('tipo_empresa')
        empresa.data_de_registro = request.POST.get('empresa_data_registro') or None
        empresa.email = request.POST.get('empresa_email')
        empresa.telefone = request.POST.get('empresa_telefone')
        empresa.logradouro = request.POST.get('empresa_logradouro')
        empresa.bairro = request.POST.get('empresa_bairro')
        empresa.cidade = request.POST.get('empresa_cidade')
        empresa.estado = request.POST.get('empresa_estado')
        empresa.cep = request.POST.get('empresa_cep')
        empresa.pais = request.POST.get('empresa_pais')
        empresa.save()

        # --------------------- USUÁRIO ---------------------
        if usuario:
            usuario.nome = request.POST.get('usuario_nome')
            usuario.username = request.POST.get('usuario_username')
            usuario.telefone = request.POST.get('usuario_telefone')
            usuario.email = request.POST.get('usuario_email')
            usuario.senha = request.POST.get('usuario_senha')
            usuario.data_de_registro = request.POST.get('usuario_data_registro') or None
            usuario.logradouro = request.POST.get('usuario_logradouro')
            usuario.bairro = request.POST.get('usuario_bairro')
            usuario.cidade = request.POST.get('usuario_cidade')
            usuario.estado = request.POST.get('usuario_estado')
            usuario.cep = request.POST.get('usuario_cep')
            usuario.pais = request.POST.get('usuario_pais')
            usuario.save()

        messages.success(request, 'Dados atualizados com sucesso!')
        return redirect('detalhe_cliente', cnpj=empresa.cnpj)

    return render(request, 'editar_cliente.html', {
        'empresa': empresa,
        'usuario': usuario,
        'relacoes': relacoes,
    })

# gestão impostos cont
def gestao_impostos_cont(request):  
    return render(request, 'gestao_impostos_cont.html')

# gestão tarefas cont
def gestao_tarefas_cont(request):
    # só contador/empresário acessa
    if request.session.get('tipo_de_usuario') not in ['contador', 'cliente']:
        return redirect('login')

    # ---------- CRIAR NOVA TAREFA (POST do modal) ----------
    if request.method == 'POST':
        empresa_cnpj = request.POST.get('empresa_cnpj')
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        status = request.POST.get('status')
        prazo_raw = request.POST.get('prazo')
        nivel_prioridade = request.POST.get('nivel_de_prioridade')


        # converte data de prazo
        prazo = None
        if prazo_raw:
            try:
                prazo = date.fromisoformat(prazo_raw)
            except ValueError:
                prazo = None

        # responsável: usuário logado (contador)
        usuario = None
        usuario_id = request.session.get('usuario_id')
        if usuario_id:
            try:
                usuario = Usuario.objects.get(pk=usuario_id)
            except Usuario.DoesNotExist:
                usuario = None

        # empresa da tarefa
        empresa = None
        if empresa_cnpj:
            empresa = Empresa.objects.filter(cnpj=empresa_cnpj).first()

        Tarefa.objects.create(
            usuario=usuario,
            empresa_cnpj=empresa,
            titulo=titulo,
            descricao=descricao,
            status=status,
            nivel_de_prioridade=nivel_prioridade,  
            criado_em=date.today(),
            prazo=prazo,
        )

        messages.success(request, 'Tarefa criada com sucesso.')
        return redirect('gestao_tarefas_cont')

    # ---------- LISTAR TAREFAS (GET) ----------
    tarefas = (
        Tarefa.objects
        .select_related('empresa_cnpj')
        .order_by('prazo', 'id')
    )

    # para o select do modal
    empresas = Empresa.objects.order_by('nome_fantasia')

    return render(
        request,
        'gestao_tarefas_cont.html',
        {
            'tarefas': tarefas,
            'empresas': empresas,
        }
    )

#detalhes das tarefas
def detalhe_tarefa(request, tarefa_id):
    # garante que só contador/empresário veja
    if request.session.get('tipo_de_usuario') not in ['contador', 'cliente']:
        return redirect('login')

    tarefa = get_object_or_404(
        Tarefa.objects.select_related('empresa_cnpj', 'usuario'),
        pk=tarefa_id
    )

    empresa = tarefa.empresa_cnpj
    usuario = tarefa.usuario

    context = {
        'tarefa': tarefa,
        'empresa': empresa,
        'usuario': usuario,
    }
    return render(request, 'detalhe_tarefa.html', context)

#editar tarefas

def editar_tarefa(request, tarefa_id):
    # só contador/empresário pode editar
    if request.session.get('tipo_de_usuario') not in ['contador', 'cliente']:
        return redirect('login')

    tarefa = get_object_or_404(
        Tarefa.objects.select_related('empresa_cnpj', 'usuario'),
        id=tarefa_id
    )

    if request.method == 'POST':
        tarefa.titulo = request.POST.get('titulo')
        tarefa.descricao = request.POST.get('descricao')
        tarefa.status = request.POST.get('status')
        tarefa.nivel_de_prioridade = request.POST.get('nivel_de_prioridade')

        prazo_raw = request.POST.get('prazo')
        if prazo_raw:
            try:
                tarefa.prazo = date.fromisoformat(prazo_raw)
            except ValueError:
                
                messages.warning(request, 'Data de prazo inválida. Mantido valor anterior.')

        tarefa.save()
        messages.success(request, 'Tarefa atualizada com sucesso!')
        return redirect('detalhe_tarefa', tarefa_id=tarefa.id)

    # GET → exibe o formulário preenchido
    return render(request, 'editar_tarefa.html', {
        'tarefa': tarefa,
    })

#excluir tarefas

def excluir_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)

    
    if request.session.get('tipo_de_usuario') not in ['contador', 'cliente']:
        return redirect('login')

    if request.method == 'POST':
        empresa_nome = tarefa.empresa_cnpj.nome_fantasia if tarefa.empresa_cnpj else ''
        tarefa.delete()
        messages.success(
            request,
            f'Tarefa da empresa "{empresa_nome}" excluída com sucesso.'
        )
        return redirect('gestao_tarefas_cont')

    # GET → mostra tela de confirmação
    return render(request, 'confirmar_exclusao_tarefa.html', {
        'tarefa': tarefa,
    })

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