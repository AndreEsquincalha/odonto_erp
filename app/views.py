# views.py
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import F, Q
from pacientes.models import Paciente
from consultas.models import Consulta
from financeiro.models import Fatura, Pagamento
from estoque.models import ItemEstoque
from prontuario.models import EvolucaoClinica, Anexo, Receita
from tratamentos.models import ProcedimentoExecutado

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoje = timezone.localdate()  # data local (respeita TIME_ZONE/USE_TZ)

        # KPIs
        ctx["total_pacientes"] = Paciente.objects.count()
        ctx["consultas_hoje"] = (
            Consulta.objects.filter(inicio__date=hoje).count()
        )
        # pendentes = ABERTA ou PARCIAL
        ctx["faturas_pendentes"] = Fatura.objects.filter(
            status__in=[Fatura.Status.ABERTA, Fatura.Status.PARCIAL]
        ).count()
        ctx["itens_alerta"] = ItemEstoque.objects.filter(
            qtd_atual__lt=F("qtd_minima")
        ).count()

        # Próximas consultas de HOJE (top 5)
        ctx["proximas_consultas"] = (
            Consulta.objects.filter(inicio__date=hoje)
            .select_related("paciente")
            .order_by("inicio")[:5]
        )

        # Atividade recente (últimos eventos diversos, top 8)
        atividades = []

        for ev in (
            EvolucaoClinica.objects.select_related("consulta", "consulta__paciente")
            .order_by("-criado_em")[:8]
        ):
            atividades.append({
                "descricao": f"Evolução clínica de {ev.consulta.paciente.nome}",
                "timestamp": ev.criado_em,
            })

        for an in (
            Anexo.objects.select_related("paciente", "consulta")
            .order_by("-criado_em")[:8]
        ):
            atividades.append({
                "descricao": f"Anexo para {an.paciente.nome}",
                "timestamp": an.criado_em,
            })

        for rc in (
            Receita.objects.select_related("consulta", "consulta__paciente")
            .order_by("-criado_em")[:8]
        ):
            atividades.append({
                "descricao": f"Receita emitida para {rc.consulta.paciente.nome}",
                "timestamp": rc.criado_em,
            })

        for pe in (
            ProcedimentoExecutado.objects.select_related("consulta", "consulta__paciente", "procedimento")
            .order_by("-realizado_em")[:8]
        ):
            atividades.append({
                "descricao": f"Procedimento executado ({pe.procedimento.nome}) - {pe.consulta.paciente.nome}",
                "timestamp": pe.realizado_em,
            })

        for ft in Fatura.objects.select_related("paciente").order_by("-criado_em")[:8]:
            atividades.append({
                "descricao": f"Fatura criada para {ft.paciente.nome} ({ft.get_status_display()})",
                "timestamp": ft.criado_em,
            })

        for pg in Pagamento.objects.select_related("fatura", "fatura__paciente").order_by("-pago_em")[:8]:
            atividades.append({
                "descricao": f"Pagamento {pg.get_metodo_pagamento_display()} de R$ {pg.valor:.2f} — {pg.fatura.paciente.nome}",
                "timestamp": pg.pago_em,
            })

        # ordena por timestamp desc e limita a 8 entradas
        atividades.sort(key=lambda x: x["timestamp"], reverse=True)
        ctx["atividades_recentes"] = atividades[:8]

        return ctx
