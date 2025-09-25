# financeiro/admin.py
from django.contrib import admin
from django.db.models import Sum
from .models import Fatura, Pagamento


# ==========
# Inlines
# ==========
class PagamentoInline(admin.TabularInline):
    model = Pagamento
    extra = 0
    fields = ("metodo_pagamento", "valor", "parcela", "pago_em")
    readonly_fields = ("pago_em",)
    ordering = ("-pago_em",)
    show_change_link = True


# ==========
# Fatura
# ==========
@admin.register(Fatura)
class FaturaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "paciente",
        "origem",
        "valor_formatado",
        "total_pago_formatado",
        "saldo_formatado",
        "status",
        "criado_em",
    )
    list_filter = ("status", "origem", "criado_em")
    search_fields = ("paciente__nome", "numero_nfse", "origem")
    ordering = ("-criado_em",)
    date_hierarchy = "criado_em"
    list_per_page = 25
    autocomplete_fields = ("paciente",)
    list_select_related = ("paciente",)
    readonly_fields = ("criado_em",)
    inlines = [PagamentoInline]

    # ---------
    # Helpers de total/saldo
    # ---------
    def _total_pago(self, obj: Fatura):
        agg = obj.pagamentos.aggregate(total=Sum("valor"))
        return agg["total"] or 0

    @admin.display(description="Total pago")
    def total_pago_formatado(self, obj: Fatura):
        total = self._total_pago(obj)
        return f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @admin.display(description="Saldo")
    def saldo_formatado(self, obj: Fatura):
        saldo = (obj.valor or 0) - self._total_pago(obj)
        return f"R$ {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @admin.display(description="Valor")
    def valor_formatado(self, obj: Fatura):
        return f"R$ {obj.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # ---------
    # Ações em massa de status
    # ---------
    actions = ["marcar_aberta", "marcar_parcial", "marcar_paga", "marcar_cancelada"]

    def _set_status(self, request, queryset, status):
        updated = queryset.update(status=status)
        self.message_user(request, f"Status atualizado em {updated} fatura(s).")

    def marcar_aberta(self, request, queryset):
        self._set_status(request, queryset, Fatura.Status.ABERTA)
    marcar_aberta.short_description = "Marcar como Aberta"

    def marcar_parcial(self, request, queryset):
        self._set_status(request, queryset, Fatura.Status.PARCIAL)
    marcar_parcial.short_description = "Marcar como Parcial"

    def marcar_paga(self, request, queryset):
        self._set_status(request, queryset, Fatura.Status.PAGA)
    marcar_paga.short_description = "Marcar como Paga"

    def marcar_cancelada(self, request, queryset):
        self._set_status(request, queryset, Fatura.Status.CANCELADA)
    marcar_cancelada.short_description = "Marcar como Cancelada"


# ==========
# Pagamento
# ==========
@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "fatura", "paciente", "metodo_pagamento", "valor_formatado", "parcela", "pago_em")
    list_filter = ("metodo_pagamento", "pago_em", "fatura__status")
    search_fields = ("fatura__paciente__nome",)
    ordering = ("-pago_em",)
    date_hierarchy = "pago_em"
    list_per_page = 25
    autocomplete_fields = ("fatura",)
    list_select_related = ("fatura", "fatura__paciente")
    readonly_fields = ("pago_em",)

    @admin.display(description="Paciente", ordering="fatura__paciente__nome")
    def paciente(self, obj: Pagamento):
        return obj.fatura.paciente

    @admin.display(description="Valor")
    def valor_formatado(self, obj: Pagamento):
        return f"R$ {obj.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
