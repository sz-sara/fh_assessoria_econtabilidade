"""
URL configuration for econtabilidade project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('', views.index, name='index'),
    path('consulta_das_cliente/', views.consulta_das_cliente, name='consulta_das_cliente'),
    path('consulta_das_cont/', views.consulta_das_cont, name='consulta_das_cont'),
    path('dashboard_cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('dashboard_cont/', views.dashboard_cont, name='dashboard_cont'),
    path('DASMEI_cliente/', views.DASMEI_cliente, name='DASMEI_cliente'),
    path('DASMEI_cont/', views.DASMEI_cont, name='DASMEI_cont'),
    path('gestao_clientes_cont/', views.gestao_clientes_cont, name='gestao_clientes_cont'),
    path('gestao_impostos_cont/', views.gestao_impostos_cont, name='gestao_impostos_cont'),
    path('gestao_tarefas_cont/', views.gestao_tarefas_cont, name='gestao_tarefas_cont'),
    path('gestaodocs/', views.gestaodocs, name='gestaodocs'),
    path('notificacoes_cliente/', views.notificacoes_cliente, name='notificacoes_cliente'),
    path('notificacoes_cont/', views.notificacoes_cont, name='notificacoes_cont'),
    path('redefinicao', views.redefinicao, name='redefinicao'),
    path('usuario', views.usuario, name='usuario'),
]
