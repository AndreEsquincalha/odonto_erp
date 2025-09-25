# pacientes/admin.py
from django.contrib import admin
from datetime import date
from .models import Paciente


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    # tabela
    list_display = (
        "nome",
        "cpf",
        "telefone",
        "email",
        "idade",
        "criado_em",
        "atualizado_em",
    )
    list_select_related = ()
    list_per_page = 25
    ordering = ("nome",)
    date_hierarchy = "criado_em"

    # busca e filtros
    search_fields = ("nome", "cpf", "email", "telefone")
    list_filter = ("criado_em", "atualizado_em", "data_nascimento")

    # edição
    readonly_fields = ("criado_em", "atualizado_em")
    fieldsets = (
        ("Dados do paciente", {
            "fields": ("nome", "cpf", "data_nascimento"),
        }),
        ("Contato", {
            "fields": ("telefone", "email", "endereco"),
        }),
        ("Metadados", {
            "classes": ("collapse",),
            "fields": ("criado_em", "atualizado_em"),
        }),
    )

    @admin.display(description="Idade", ordering="data_nascimento")
    def idade(self, obj: Paciente):
        """Calcula idade aproximada a partir da data de nascimento."""
        if not obj.data_nascimento:
            return "-"
        today = date.today()
        years = today.year - obj.data_nascimento.year
        # ajusta se ainda não fez aniversário no ano
        if (today.month, today.day) < (obj.data_nascimento.month, obj.data_nascimento.day):
            years -= 1
        return years
