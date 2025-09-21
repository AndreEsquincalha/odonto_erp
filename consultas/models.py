from django.db import models
from pacientes.models import Paciente

class Consulta(models.Model):
    class Status(models.TextChoices):
        AGENDADA = "AG", "Agendada"
        CONFIRMADA = "CF", "Confirmada"
        EM_ANDAMENTO = "EA", "Em andamento"
        CONCLUIDA = "CO", "Concluída"
        CANCELADA = "CA", "Cancelada"
        FALTOU = "FA", "Faltou"


    paciente = models.ForeignKey(Paciente, verbose_name=("Paciente"), on_delete=models.PROTECT)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.AGENDADA
    )
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    sala = models.CharField(max_length=30)
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['inicio']
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"

    def __str__(self):
        return f"{self.get_status_display()} - {self.paciente.nome} ({self.inicio:%d/%m/%Y %H:%M})"
