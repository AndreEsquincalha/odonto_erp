# tratamentos/admin.py
from django.contrib import admin
from .models import (
    PlanoTratamento,
    CatalogoProcedimento,
    ProcedimentoPlanejado,
    ProcedimentoExecutado,
    Orcamento,
)

# =========================
# Inlines
# =========================
class ProcedimentoPlanejadoInline(admin.TabularInline):
    model = ProcedimentoPlanejado
    extra = 0
    fields = ("procedimento", "dente_superficie", "quantidade", "valor_unitario", "status", "criado_em")
    readonly_fields = ("criado_em",)
    autocomplete_fields = ("procedimento",)
    show_change_link = True
    ordering = ("-id",)


class OrcamentoInline(admin.TabularInline):
    model = Orcamento
    extra = 0
    fields = ("total", "desconto", "validade", "aprovado_em")
    readonly_fields = ()
    show_change_link = True
    ordering = ("-id",)


# =========================
# Plano de Tratamento
# =========================
@admin.register(PlanoTratamento)
class PlanoTratamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "paciente", "status", "total_planejado", "criado_em")
    list_filter = ("status", "criado_em")
    search_fields = ("paciente__nome",)
    ordering = ("-criado_em",)
    date_hierarchy = "criado_em"
    autocomplete_fields = ("paciente",)
    list_select_related = ("paciente",)
    readonly_fields = ("criado_em",)
    inlines = [ProcedimentoPlanejadoInline, OrcamentoInline]
    list_per_page = 25

    @admin.display(description="Total planejado")
    def total_planejado(self, obj: PlanoTratamento):
        # soma quantidade * valor_unitario dos planejados
        total = 0
        for p in obj.procedimentos.all():
            total += (p.quantidade or 0) * (p.valor_unitario or 0)
        return f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# =========================
# Catálogo de Procedimentos
# =========================
@admin.register(CatalogoProcedimento)
class CatalogoProcedimentoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nome", "duracao_min", "preco_base")
    list_filter = ("duracao_min",)
    search_fields = ("codigo", "nome")
    ordering = ("nome",)
    list_per_page = 25


# =========================
# Procedimento Planejado
# =========================
@admin.register(ProcedimentoPlanejado)
class ProcedimentoPlanejadoAdmin(admin.ModelAdmin):
    list_display = ("id", "plano", "paciente", "procedimento", "dente_superficie", "quantidade", "valor_unitario", "valor_total", "status", "criado_em")
    list_filter = ("status", "criado_em", "procedimento")
    search_fields = ("plano__paciente__nome", "procedimento__nome", "dente_superficie")
    ordering = ("-id",)
    date_hierarchy = "criado_em"
    autocomplete_fields = ("plano", "procedimento")
    list_select_related = ("plano", "plano__paciente", "procedimento")
    readonly_fields = ("criado_em",)
    list_per_page = 25

    @admin.display(description="Paciente", ordering="plano__paciente__nome")
    def paciente(self, obj: ProcedimentoPlanejado):
        return obj.plano.paciente

    @admin.display(description="Valor total")
    def valor_total(self, obj: ProcedimentoPlanejado):
        total = (obj.quantidade or 0) * (obj.valor_unitario or 0)
        return f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Ações em massa para status
    actions = ["marcar_pendente", "marcar_aprovado", "marcar_executado", "marcar_cancelado"]

    def _set_status(self, request, queryset, status):
        updated = queryset.update(status=status)
        self.message_user(request, f"Status atualizado em {updated} procedimento(s).")

    def marcar_pendente(self, request, queryset):
        self._set_status(request, queryset, ProcedimentoPlanejado.Status.PENDENTE)
    marcar_pendente.short_description = "Marcar como Pendente"

    def marcar_aprovado(self, request, queryset):
        self._set_status(request, queryset, ProcedimentoPlanejado.Status.APROVADO)
    marcar_aprovado.short_description = "Marcar como Aprovado"

    def marcar_executado(self, request, queryset):
        self._set_status(request, queryset, ProcedimentoPlanejado.Status.EXECUTADO)
    marcar_executado.short_description = "Marcar como Executado"

    def marcar_cancelado(self, request, queryset):
        self._set_status(request, queryset, ProcedimentoPlanejado.Status.CANCELADO)
    marcar_cancelado.short_description = "Marcar como Cancelado"


# =========================
# Procedimento Executado
# =========================
@admin.register(ProcedimentoExecutado)
class ProcedimentoExecutadoAdmin(admin.ModelAdmin):
    list_display = ("id", "consulta", "paciente", "procedimento", "dente", "superficie", "quantidade", "valor_unitario", "valor_total", "realizado_em")
    list_filter = ("realizado_em", "procedimento")
    search_fields = ("consulta__paciente__nome", "procedimento__nome", "dente")
    ordering = ("-realizado_em",)
    date_hierarchy = "realizado_em"
    autocomplete_fields = ("consulta", "planejado", "procedimento")
    list_select_related = ("consulta", "consulta__paciente", "procedimento", "planejado")
    readonly_fields = ("realizado_em",)
    list_per_page = 25

    @admin.display(description="Paciente", ordering="consulta__paciente__nome")
    def paciente(self, obj: ProcedimentoExecutado):
        return obj.consulta.paciente

    @admin.display(description="Valor total")
    def valor_total(self, obj: ProcedimentoExecutado):
        total = (obj.quantidade or 0) * (obj.valor_unitario or 0)
        return f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# =========================
# Orçamento
# =========================
@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "plano", "paciente", "total_formatado", "desconto_formatado", "validade", "aprovado_em")
    list_filter = ("validade", "aprovado_em")
    search_fields = ("plano__paciente__nome",)
    ordering = ("-id",)
    date_hierarchy = "aprovado_em"
    autocomplete_fields = ("plano",)
    list_select_related = ("plano", "plano__paciente")
    list_per_page = 25

    @admin.display(description="Paciente", ordering="plano__paciente__nome")
    def paciente(self, obj: Orcamento):
        return obj.plano.paciente

    @admin.display(description="Total")
    def total_formatado(self, obj: Orcamento):
        return f"R$ {obj.total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @admin.display(description="Desconto")
    def desconto_formatado(self, obj: Orcamento):
        return f"R$ {obj.desconto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
