from django.contrib import admin

# Register your models here.
from .models import (
    Usuario,
    Empresa,
    Documento,
    DocumentoEmpresa,
    Imposto,
    EmpresasUsuarioCliente,
    Tarefa,
    Notificacao,
)

admin.site.register(Usuario)
admin.site.register(Empresa)
admin.site.register(Documento)
admin.site.register(DocumentoEmpresa)
admin.site.register(Imposto)
admin.site.register(EmpresasUsuarioCliente)
admin.site.register(Tarefa)
admin.site.register(Notificacao)
