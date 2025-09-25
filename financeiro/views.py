# financeiro/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Fatura, Pagamento
from .forms import FaturaForm, PagamentoForm

class FaturaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Fatura
    template_name = "financeiro/fatura_list.html"
    context_object_name = "faturas"
    paginate_by = 20
    permission_required = "financeiro.view_fatura"

    def get_queryset(self):
        qs = super().get_queryset().select_related("paciente")
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs

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
