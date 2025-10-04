# financeiro/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Fatura, Pagamento
from .forms import FaturaForm, PagamentoForm


from pacientes.models import Paciente
from django.db.models import Q

class FaturaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Fatura
    template_name = "financeiro/fatura_list.html"
    context_object_name = "faturas"
    paginate_by = 20
    permission_required = "financeiro.view_fatura"

    def get_queryset(self):
        qs = super().get_queryset().select_related("paciente")

        # --- NOVO: filtra pelo paciente quando vier na URL ---
        paciente_id = self.request.GET.get("paciente")
        if paciente_id:
            try:
                qs = qs.filter(paciente_id=int(paciente_id))
            except (TypeError, ValueError):
                pass

        # filtro por status (já existia)
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)

        # (Opcional) busca simples do search_filter (q)
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(paciente__nome__icontains=q) |
                Q(id__icontains=q)
            )

        return qs.order_by("-criado_em", "-id")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # (Opcional) exibir “chip” com o paciente filtrado
        paciente_id = self.request.GET.get("paciente")
        ctx["paciente_filtro"] = None
        if paciente_id and str(paciente_id).isdigit():
            ctx["paciente_filtro"] = Paciente.objects.filter(pk=paciente_id).first()
        return ctx

class FaturaDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Fatura
    template_name = "financeiro/fatura_detail.html"
    context_object_name = "fatura"
    permission_required = "financeiro.view_fatura"

class FaturaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Fatura
    form_class = FaturaForm
    template_name = "financeiro/fatura_form.html"
    permission_required = "financeiro.add_fatura"
    success_url = reverse_lazy("financeiro:fatura_list")

class FaturaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Fatura
    form_class = FaturaForm
    template_name = "financeiro/fatura_form.html"
    permission_required = "financeiro.change_fatura"
    success_url = reverse_lazy("financeiro:fatura_list")

class PagamentoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Pagamento
    form_class = PagamentoForm
    template_name = "financeiro/pagamento_form.html"
    permission_required = "financeiro.add_pagamento"

    def get_initial(self):
        initial = super().get_initial()
        if "fatura" in self.request.GET:
            initial["fatura"] = self.request.GET.get("fatura")
        return initial

    def get_success_url(self):
        messages.success(self.request, "Pagamento registrado.")
        return reverse_lazy("financeiro:fatura_detail", kwargs={"pk": self.object.fatura_id})
