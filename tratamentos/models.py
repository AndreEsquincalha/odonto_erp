from django.db import models
from pacientes.models import Paciente
from consultas.models import Consulta

class PlanoTratamento(models.Model):
    class Status(models.TextChoices):
        RASCUNHO = "RA", "Rascunho"
        AGUARDANDO = "AG", "Aguardando aprovação"
        APROVADO = "AP", "Aprovado"
        EM_ANDAMENTO = "EA", "Em andamento"
        CONCLUIDO = "CO", "Concluído"
        CANCELADO = "CA", "Cancelado"

    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name="planos_tratamento")
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.RASCUNHO
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Plano de Tratamento"
        verbose_name_plural = "Planos de Tratamento"

    def __str__(self):
        return f"Plano de {self.paciente.nome} - {self.get_status_display()}"
    
class CatalogoProcedimento(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nome = models.CharField(max_length=120)
    duracao_min = models.PositiveIntegerField(default=30)
    preco_base = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Procedimento (Catálogo)"
        verbose_name_plural = "Procedimentos (Catálogo)"

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class ProcedimentoPlanejado(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "PE", "Pendente"
        APROVADO = "AP", "Aprovado"
        EXECUTADO = "EX", "Executado"
        CANCELADO = "CA", "Cancelado"

    plano = models.ForeignKey(PlanoTratamento, on_delete=models.CASCADE, related_name="procedimentos")
    procedimento = models.ForeignKey(CatalogoProcedimento, on_delete=models.PROTECT, related_name="planejados")
    dente_superficie = models.CharField(max_length=8, blank=True)  # ex.: 36-O
    quantidade = models.PositiveIntegerField(default=1)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDENTE)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["plano_id"]
        verbose_name = "Procedimento Planejado"
        verbose_name_plural = "Procedimentos Planejados"

    def __str__(self):
        return f"{self.procedimento.nome} ({self.dente_superficie or '-'})"


class ProcedimentoExecutado(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.PROTECT, related_name="procedimentos_executados")
    planejado = models.ForeignKey(ProcedimentoPlanejado, on_delete=models.SET_NULL, null=True, blank=True, related_name="execucoes")
    procedimento = models.ForeignKey(CatalogoProcedimento, on_delete=models.PROTECT, related_name="executados")
    dente = models.CharField(max_length=2)        # pode usar choices FDI se preferir
    superficie = models.CharField(max_length=1, blank=True)
    quantidade = models.PositiveIntegerField(default=1)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    realizado_em = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True)

    class Meta:
        ordering = ["-realizado_em"]
        verbose_name = "Procedimento Executado"
        verbose_name_plural = "Procedimentos Executados"

    def __str__(self):
        return f"{self.procedimento.nome} dente {self.dente} ({self.realizado_em:%d/%m/%Y})"
    
class Orcamento(models.Model):
    plano = models.ForeignKey(PlanoTratamento, on_delete=models.CASCADE, related_name="orcamentos")
    total = models.DecimalField(max_digits=10, decimal_places=2)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    validade = models.DateField()
    aprovado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Orçamento"
        verbose_name_plural = "Orçamentos"

    def __str__(self):
        return f"Orçamento do plano #{self.plano_id} - Total {self.total}"