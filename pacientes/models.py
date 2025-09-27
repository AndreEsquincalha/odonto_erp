from django.db import models
from django.utils import timezone

class Paciente(models.Model):
    nome = models.CharField(max_length=250)
    cpf = models.CharField(unique=True)
    data_nascimento = models.DateField()
    telefone = models.CharField()
    email = models.EmailField(blank=True)
    endereco = models.TextField(blank=True)

    # Controle de exclusão lógica
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return self.nome

    # Método para "excluir" logicamente
    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()
