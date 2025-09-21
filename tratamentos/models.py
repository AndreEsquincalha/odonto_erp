from django.db import models
from pacientes.models import Paciente

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