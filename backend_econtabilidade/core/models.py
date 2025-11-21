from django.db import models

class Empresa(models.Model):
    cnpj = models.CharField(db_column='CNPJ', max_length=20, primary_key=True)
    razao_social = models.CharField(db_column='Razao_social', max_length=255, blank=True, null=True)
    nome_fantasia = models.CharField(db_column='Nome_fantasia', max_length=255, blank=True, null=True)
    inscricao_municipal = models.CharField(db_column='Inscricao_municipal', max_length=50, blank=True, null=True)
    tipo_empresa = models.CharField(db_column='Tipo_Empresa', max_length=50, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)
    telefone = models.CharField(db_column='Telefone', max_length=50, blank=True, null=True)
    logradouro = models.CharField(db_column='Logradouro', max_length=255, blank=True, null=True)
    bairro = models.CharField(db_column='Bairro', max_length=100, blank=True, null=True)
    cidade = models.CharField(db_column='Cidade', max_length=100, blank=True, null=True)
    estado = models.CharField(db_column='Estado', max_length=100, blank=True, null=True)
    cep = models.CharField(db_column='CEP', max_length=20, blank=True, null=True)
    pais = models.CharField(db_column='Pais', max_length=100, blank=True, null=True)
    data_de_registro = models.DateField(db_column='Data_de_registro', blank=True, null=True)

    class Meta:
        db_table = 'Empresas'


class Usuario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    tipo_de_usuario = models.CharField(db_column='Tipo_de_usuario', max_length=50, blank=True, null=True)
    cpf = models.CharField(db_column='CPF', max_length=20, unique=True, blank=True, null=True)
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)
    username = models.CharField(db_column='User', max_length=100, blank=True, null=True)
    senha = models.CharField(db_column='Senha', max_length=255, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)
    telefone = models.CharField(db_column='Telefone', max_length=50, blank=True, null=True)
    logradouro = models.CharField(db_column='Logradouro', max_length=255, blank=True, null=True)
    bairro = models.CharField(db_column='Bairro', max_length=100, blank=True, null=True)
    cidade = models.CharField(db_column='Cidade', max_length=100, blank=True, null=True)
    estado = models.CharField(db_column='Estado', max_length=100, blank=True, null=True)
    cep = models.CharField(db_column='CEP', max_length=20, blank=True, null=True)
    pais = models.CharField(db_column='Pais', max_length=100, blank=True, null=True)
    data_de_registro = models.DateField(db_column='Data_de_registro', blank=True, null=True)

    class Meta:
        db_table = 'Usuario'


class Documento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    tipo_documento = models.CharField(db_column='Tipo_Documento', max_length=100, blank=True, null=True)
    titulo = models.CharField(db_column='Titulo', max_length=255, blank=True, null=True)
    url_documento = models.CharField(db_column='Url_documento', max_length=255, blank=True, null=True)
    empresa_cnpj = models.ForeignKey(
        'Empresa',
        to_field='cnpj',
        db_column='Empresa_CNPJ',
        on_delete=models.CASCADE,
        related_name='documentos',
        blank=True, null=True
    )
    submetido_por = models.ForeignKey(
        'Usuario',
        db_column='Submetido_por',
        on_delete=models.SET_NULL,
        related_name='documentos_submetidos',
        blank=True, null=True
    )

    class Meta:
        db_table = 'Documentos'


class DocumentoEmpresa(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    empresa_cnpj = models.ForeignKey(
        'Empresa',
        to_field='cnpj',
        db_column='Empresa_CNPJ',
        on_delete=models.CASCADE,
        related_name='documentos_empresas'
    )
    documento = models.ForeignKey(
        'Documento',
        db_column='Documento_ID',
        on_delete=models.CASCADE,
        related_name='empresas_relacionadas'
    )

    class Meta:
        db_table = 'Documentos_Empresa'


class Imposto(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    documento = models.ForeignKey(
        'Documento',
        db_column='Documento_id',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='impostos'
    )
    comprovante_pagamento = models.IntegerField(db_column='Comprovante_pagamento', blank=True, null=True)
    empresa_cnpj = models.ForeignKey(
        'Empresa',
        to_field='cnpj',
        db_column='Empresa_CNPJ',
        on_delete=models.CASCADE,
        related_name='impostos'
    )
    tipo_imposto = models.CharField(db_column='Tipo_Imposto', max_length=100, blank=True, null=True)
    competencia = models.CharField(db_column='Competencia', max_length=50, blank=True, null=True)
    jurisdicao = models.CharField(db_column='Jurisdicao', max_length=100, blank=True, null=True)
    data_pagamento = models.DateField(db_column='Data_Pagamento', blank=True, null=True)
    data_vencimento = models.DateField(db_column='Data_Vencimento', blank=True, null=True)
    valor = models.DecimalField(db_column='Valor', max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Imposto'


class EmpresasUsuarioCliente(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    empresa_cnpj = models.ForeignKey(
        'Empresa',
        to_field='cnpj',
        db_column='Empresa_CNPJ',
        on_delete=models.CASCADE,
        related_name='usuarios_clientes'
    )
    tipo_usuario = models.CharField(db_column='Tipo_usuario', max_length=50, blank=True, null=True)
    usuario_cliente = models.ForeignKey(
        'Usuario',
        to_field='cpf',
        db_column='Usuario_Cliente_CPF',
        on_delete=models.CASCADE,
        related_name='empresas_como_cliente'
    )

    class Meta:
        db_table = 'Empresas_Usuario_Cliente'


class Tarefa(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    usuario = models.ForeignKey(
        'Usuario',
        db_column='Usuario_id',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tarefas'
    )
    titulo = models.CharField(db_column='Titulo', max_length=255, blank=True, null=True)
    descricao = models.TextField(db_column='Descricao', blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=50, blank=True, null=True)
    nivel_de_prioridade = models.CharField(db_column='Nivel_de_prioridade', max_length=50, blank=True, null=True)
    criado_em = models.DateField(db_column='Criado_em', blank=True, null=True)

    class Meta:
        db_table = 'Tarefa'


class Notificacao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    usuario = models.ForeignKey(
        'Usuario',
        db_column='Usuario_id',
        on_delete=models.CASCADE,
        related_name='notificacoes'
    )
    assunto = models.CharField(db_column='Assunto', max_length=255, blank=True, null=True)
    mensagem = models.TextField(db_column='Mensagem', blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=50, blank=True, null=True)
    criado_em = models.DateField(db_column='Criado_em', blank=True, null=True)

    class Meta:
        db_table = 'Notificacao'
