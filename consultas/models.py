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

class Lembrete(models.Model):
    class Canal(models.TextChoices):
        WHATSAPP = "WA", "WhatsApp"
        SMS = "SM", "SMS"
        EMAIL = "EM", "E-mail"

    class Status(models.TextChoices):
        AGENDADO = "AG", "Agendado"
        ENVIADO = "EN", "Enviado"
        FALHA = "FA", "Falha"

    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name="lembretes")
    canal = models.CharField(max_length=2, choices=Canal.choices)
    agendado_em = models.DateTimeField()
    enviado_em = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.AGENDADO)

    class Meta:
        ordering = ["-agendado_em"]
        verbose_name = "Lembrete"
        verbose_name_plural = "Lembretes"

    def __str__(self):
        return f"{self.get_canal_display()} - {self.get_status_display()} ({self.agendado_em:%d/%m/%Y %H:%M})"