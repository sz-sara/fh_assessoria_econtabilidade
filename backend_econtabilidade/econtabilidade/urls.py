from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rotas da aplicação
    path('', views.index, name='index'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),

    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
    path('redefinicao/', views.redefinicao, name='redefinicao'),

    path('consulta-das-cliente/', views.consulta_das_cliente, name='consulta_das_cliente'),
    path('consulta-das-cont/', views.consulta_das_cont, name='consulta_das_cont'),

    path('dashboard-cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('dashboard-contador/', views.dashboard_cont, name='dashboard_cont'),

    path('dasmei-cliente/', views.DASMEI_cliente, name='DASMEI_cliente'),
    path('dasmei-cont/', views.DASMEI_cont, name='DASMEI_cont'),

    path('gestao-clientes/', views.gestao_clientes_cont, name='gestao_clientes_cont'),
    path('gestao-clientes/<str:cnpj>/', views.detalhe_cliente, name='detalhe_cliente'),
    path('clientes/<str:cnpj>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<str:cnpj>/excluir/', views.excluir_cliente, name='excluir_cliente'),


    path('gestao-impostos/', views.gestao_impostos_cont, name='gestao_impostos_cont'),
    path('gestao-tarefas/', views.gestao_tarefas_cont, name='gestao_tarefas_cont'),
    path('tarefas/<int:tarefa_id>/', views.detalhe_tarefa, name='detalhe_tarefa'),
    path('tarefas/<int:tarefa_id>/editar/', views.editar_tarefa, name='editar_tarefa'),
    path('tarefas/<int:tarefa_id>/excluir/', views.excluir_tarefa, name='excluir_tarefa'),
    
    path('gestao-docs/', views.gestaodocs, name='gestaodocs'),

    path('notificacoes-cliente/', views.notificacoes_cliente, name='notificacoes_cliente'),
    path('notificacoes-contador/', views.notificacoes_cont, name='notificacoes_cont'),

    path('usuario/', views.usuario, name='usuario'),
]

