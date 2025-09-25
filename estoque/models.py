# estoque/models.py
from django.db import models
from consultas.models import Consulta

class ItemEstoque(models.Model):
    descricao = models.CharField(max_length=120)
    marca = models.CharField(max_length=60, blank=True)
    lote = models.CharField(max_length=60, blank=True)
    validade = models.DateField(null=True, blank=True)
    qtd_minima = models.PositiveIntegerField(default=0)
    qtd_atual = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["descricao"]
        verbose_name = "Item de Estoque"
        verbose_name_plural = "Itens de Estoque"

    def __str__(self):
        return f"{self.descricao} ({self.qtd_atual})"


class MovimentoEstoque(models.Model):
    class Tipo(models.TextChoices):
        ENTRADA = "IN", "Entrada"
        SAIDA = "OUT", "Saída"

    item = models.ForeignKey(ItemEstoque, on_delete=models.PROTECT, related_name="movimentos")
    tipo_movimento = models.CharField(max_length=3, choices=Tipo.choices)
    quantidade = models.PositiveIntegerField()
    motivo = models.CharField(max_length=120, blank=True)
    consulta = models.ForeignKey(Consulta, on_delete=models.SET_NULL, null=True, blank=True, related_name="movimentos_estoque")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Movimento de Estoque"
        verbose_name_plural = "Movimentos de Estoque"

    def __str__(self):
        return f"{self.get_tipo_movimento_display()} - {self.item.descricao} ({self.quantidade})"
