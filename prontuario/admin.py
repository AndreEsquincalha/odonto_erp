# prontuario/admin.py
from django.contrib import admin
from .models import (
    Odontograma,
    EvolucaoClinica,
    Anexo,
    Receita,
    TermoConsentimento,
)


@admin.register(Odontograma)
class OdontogramaAdmin(admin.ModelAdmin):
    list_display = (
        "paciente",
        "dente",
        "superficie",
        "condicao",
        "procedimento_executado",
        "criado_em",
    )
    list_filter = ("dente", "superficie", "criado_em")
    search_fields = (
        "paciente__nome",
        "condicao",
        "procedimento_executado__procedimento__nome",
    )
    ordering = ("paciente__nome", "dente", "-criado_em")
    date_hierarchy = "criado_em"
    list_per_page = 30
    list_select_related = ("paciente", "procedimento_executado")
    autocomplete_fields = ("paciente", "procedimento_executado")
    readonly_fields = ("criado_em",)


@admin.register(EvolucaoClinica)
class EvolucaoClinicaAdmin(admin.ModelAdmin):
    list_display = ("consulta", "paciente", "usuario", "preview", "criado_em")
    list_filter = ("usuario", "criado_em")
    search_fields = ("consulta__paciente__nome", "usuario__username", "anotacao")
    ordering = ("-criado_em",)
    date_hierarchy = "criado_em"
    list_select_related = ("consulta", "consulta__paciente", "usuario")
    autocomplete_fields = ("consulta", "usuario")
    readonly_fields = ("criado_em",)

    @admin.display(description="Paciente", ordering="consulta__paciente__nome")
    def paciente(self, obj):
        return obj.consulta.paciente

    @admin.display(description="Anotação")
    def preview(self, obj):
        # mostra um pedacinho da evolução na lista
        return (obj.anotacao[:60] + "…") if len(obj.anotacao) > 60 else obj.anotacao


@admin.register(Anexo)
class AnexoAdmin(admin.ModelAdmin):
    list_display = ("paciente", "consulta", "tipo_arquivo", "caminho_arquivo", "criado_em")
    list_filter = ("tipo_arquivo", "criado_em")
    search_fields = ("paciente__nome", "consulta__paciente__nome", "caminho_arquivo", "tipo_arquivo")
    ordering = ("-criado_em",)
    date_hierarchy = "criado_em"
    list_select_related = ("paciente", "consulta")
    autocomplete_fields = ("paciente", "consulta")
    readonly_fields = ("criado_em",)


@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ("consulta", "paciente", "criado_em")
    list_filter = ("criado_em",)
    search_fields = ("consulta__paciente__nome", "texto")
    ordering = ("-criado_em",)
    date_hierarchy = "criado_em"
    list_select_related = ("consulta", "consulta__paciente")
    autocomplete_fields = ("consulta",)
    readonly_fields = ("criado_em",)

    @admin.display(description="Paciente", ordering="consulta__paciente__nome")
    def paciente(self, obj):
        return obj.consulta.paciente


@admin.register(TermoConsentimento)
class TermoConsentimentoAdmin(admin.ModelAdmin):
    list_display = ("paciente", "procedimento", "assinado", "assinado_em")
    list_filter = ("assinado_em",)
    search_fields = ("paciente__nome", "procedimento__nome", "texto")
    ordering = ("-assinado_em", "paciente__nome")
    date_hierarchy = "assinado_em"
    list_select_related = ("paciente", "procedimento")
    autocomplete_fields = ("paciente", "procedimento")
    readonly_fields = ("assinado_em",)

    @admin.display(boolean=True, description="Assinado")
    def assinado(self, obj):
        return bool(obj.assinado_em)
