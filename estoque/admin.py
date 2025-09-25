# estoque/admin.py
from django.contrib import admin
from django.db.models import Sum
from .models import ItemEstoque, MovimentoEstoque


# =========================
# Inlines
# =========================
class MovimentoEstoqueInline(admin.TabularInline):
    model = MovimentoEstoque
    extra = 0
    fields = ("tipo_movimento", "quantidade", "motivo", "consulta", "criado_em")
    readonly_fields = ("criado_em",)
    autocomplete_fields = ("consulta",)
    ordering = ("-criado_em",)
    show_change_link = True


# =========================
# Item de Estoque
# =========================
@admin.register(ItemEstoque)
class ItemEstoqueAdmin(admin.ModelAdmin):
    list_display = (
        "descricao",
        "marca",
        "lote",
        "validade",
        "qtd_atual",
        "qtd_minima",
        "abaixo_minimo",
        "consumo_total",
    )
    list_filter = ("marca", "validade")
    search_fields = ("descricao", "marca", "lote")
    ordering = ("descricao",)
    list_per_page = 25
    inlines = [MovimentoEstoqueInline]

    @admin.display(boolean=True, description="Abaixo do mínimo")
    def abaixo_minimo(self, obj: ItemEstoque):
        return obj.qtd_atual < obj.qtd_minima

    @admin.display(description="Consumo total")
    def consumo_total(self, obj: ItemEstoque):
        # Soma de saídas (OUT) em movimentos
        agg = obj.movimentos.filter(tipo_movimento=MovimentoEstoque.Tipo.SAIDA).aggregate(
            total=Sum("quantidade")
        )
        total = agg["total"] or 0
        return total

    # ---- AÇÕES EM MASSA ----
    actions = ["zerar_estoque", "ajustar_para_minimo"]

    def zerar_estoque(self, request, queryset):
        updated = queryset.update(qtd_atual=0)
        self.message_user(request, f"Estoque zerado para {updated} item(ns).")
    zerar_estoque.short_description = "Zerar estoque selecionado"

    def ajustar_para_minimo(self, request, queryset):
        count = 0
        for item in queryset:
            if item.qtd_atual < item.qtd_minima:
                item.qtd_atual = item.qtd_minima
                item.save(update_fields=["qtd_atual"])
                count += 1
        self.message_user(request, f"Ajustado para o mínimo em {count} item(ns).")
    ajustar_para_minimo.short_description = "Ajustar itens abaixo do mínimo para o mínimo"


# =========================
# Movimento de Estoque
# =========================
@admin.register(MovimentoEstoque)
class MovimentoEstoqueAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "tipo_movimento",
        "quantidade",
        "motivo",
        "consulta",
        "criado_em",
    )
    list_filter = ("tipo_movimento", "criado_em")
    search_fields = ("item__descricao", "motivo", "consulta__paciente__nome")
    ordering = ("-criado_em",)
    date_hierarchy = "criado_em"
    list_per_page = 25
    autocomplete_fields = ("item", "consulta")
    list_select_related = ("item", "consulta")
    readonly_fields = ("criado_em",)
