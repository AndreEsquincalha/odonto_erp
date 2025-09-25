# financeiro/models.py
from django.db import models
from pacientes.models import Paciente

class Fatura(models.Model):
    class Status(models.TextChoices):
        ABERTA = "AB", "Aberta"
        PARCIAL = "PA", "Parcial"
        PAGA = "PG", "Paga"
        CANCELADA = "CA", "Cancelada"

    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name="faturas")
    origem = models.CharField(max_length=60, blank=True)  # ex.: consulta, plano, avulsa
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ABERTA)
    numero_nfse = models.CharField(max_length=60, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Fatura"
        verbose_name_plural = "Faturas"

    def __str__(self):
        return f"Fatura #{self.id} - {self.paciente.nome} ({self.get_status_display()})"


class Pagamento(models.Model):
    class Metodo(models.TextChoices):
        PIX = "PX", "PIX"
        CARTAO = "CC", "Cartão"
        DINHEIRO = "DN", "Dinheiro"
        BOLETO = "BL", "Boleto"

    fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE, related_name="pagamentos")
    metodo_pagamento = models.CharField(max_length=2, choices=Metodo.choices)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    pago_em = models.DateTimeField(auto_now_add=True)
    parcela = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["-pago_em"]
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"

    def __str__(self):
        return f"{self.get_metodo_pagamento_display()} - {self.valor} em {self.pago_em:%d/%m/%Y}"
