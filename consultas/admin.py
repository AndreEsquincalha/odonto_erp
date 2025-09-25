# consultas/admin.py
from django.contrib import admin
from .models import Consulta, Lembrete


class LembreteInline(admin.TabularInline):
    model = Lembrete
    extra = 0
    fields = ("canal", "status", "agendado_em", "enviado_em")
    readonly_fields = ()
    ordering = ("-agendado_em",)


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = (
        "inicio",
        "fim",
        "paciente",
        "status",
        "sala",
        "qtd_lembretes",
        "criado_em",
    )
    list_filter = ("status", "sala", "inicio", "fim", "criado_em")
    search_fields = ("paciente__nome", "sala", "observacoes")
    ordering = ("-inicio",)
    date_hierarchy = "inicio"
    list_per_page = 25
    autocomplete_fields = ("paciente",)
    readonly_fields = ("criado_em",)
    list_select_related = ("paciente",)
    inlines = [LembreteInline]

    @admin.display(description="Lembretes")
    def qtd_lembretes(self, obj: Consulta) -> int:
        return obj.lembretes.count()

    # ---- AÇÕES RÁPIDAS DE STATUS ----
    actions = [
        "marcar_agendada",
        "marcar_confirmada",
        "marcar_em_andamento",
        "marcar_concluida",
        "marcar_cancelada",
        "marcar_faltou",
    ]

    def _set_status(self, request, queryset, status):
        updated = queryset.update(status=status)
        self.message_user(request, f"Status atualizado em {updated} consulta(s).")

    def marcar_agendada(self, request, queryset):
        self._set_status(request, queryset, Consulta.Status.AGENDADA)
    marcar_agendada.short_description = "Marcar como Agendada"

    def marcar_confirmada(self, request, queryset):
        self._set_status(request, queryset, Consulta.Status.CONFIRMADA)
    marcar_confirmada.short_description = "Marcar como Confirmada"

    def marcar_em_andamento(self, request, queryset):
        self._set_status(request, queryset, Consulta.Status.EM_ANDAMENTO)
    marcar_em_andamento.short_description = "Marcar como Em andamento"

    def marcar_concluida(self, request, queryset):
        self._set_status(request, queryset, Consulta.Status.CONCLUIDA)
    marcar_concluida.short_description = "Marcar como Concluída"

    def marcar_cancelada(self, request, queryset):
        self._set_status(request, queryset, Consulta.Status.CANCELADA)
    marcar_cancelada.short_description = "Marcar como Cancelada"

    def marcar_faltou(self, request, queryset):
        self._set_status(request, queryset, Consulta.Status.FALTOU)
    marcar_faltou.short_description = "Marcar como Faltou"


@admin.register(Lembrete)
class LembreteAdmin(admin.ModelAdmin):
    list_display = ("consulta", "canal", "status", "agendado_em", "enviado_em")
    list_filter = ("canal", "status", "agendado_em", "enviado_em")
    search_fields = ("consulta__paciente__nome",)
    ordering = ("-agendado_em",)
    autocomplete_fields = ("consulta",)
    list_select_related = ("consulta",)
