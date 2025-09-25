# consultas/views.py
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import redirect, get_object_or_404
from .models import Consulta, Lembrete
from .forms import ConsultaForm, LembreteForm

class SearchMixin:
    search_param = "q"
    search_fields = []
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get(self.search_param, "").strip()
        if q:
            from django.db.models import Q
            query = Q()
            for f in self.search_fields:
                query |= Q(**{f"{f}__icontains": q})
            qs = qs.filter(query)
        return qs

class ConsultaListView(LoginRequiredMixin, PermissionRequiredMixin, SearchMixin, ListView):
    model = Consulta
    template_name = "consultas/consulta_list.html"
    context_object_name = "consultas"
    paginate_by = 20
    permission_required = "consultas.view_consulta"
    search_fields = ["paciente__nome", "sala", "observacoes", "status"]

    def get_queryset(self):
        qs = super().get_queryset().select_related("paciente")
        # filtros simples (status, data)
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        start = self.request.GET.get("start")
        end = self.request.GET.get("end")
        if start:
            qs = qs.filter(inicio__date__gte=start)
        if end:
            qs = qs.filter(inicio__date__lte=end)
        return qs.order_by("inicio")

class ConsultaDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Consulta
    template_name = "consultas/consulta_detail.html"
    context_object_name = "consulta"
    permission_required = "consultas.view_consulta"

class ConsultaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = "consultas/consulta_form.html"
    permission_required = "consultas.add_consulta"
    success_url = reverse_lazy("consultas:list")

    def form_valid(self, form):
        messages.success(self.request, "Consulta criada com sucesso.")
        return super().form_valid(form)

class ConsultaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = "consultas/consulta_form.html"
    permission_required = "consultas.change_consulta"
    success_url = reverse_lazy("consultas:list")

    def form_valid(self, form):
        messages.success(self.request, "Consulta atualizada.")
        return super().form_valid(form)

class ConsultaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Consulta
    template_name = "consultas/consulta_confirm_delete.html"
    permission_required = "consultas.delete_consulta"
    success_url = reverse_lazy("consultas:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Consulta excluída.")
        return super().delete(request, *args, **kwargs)

# Ações rápidas (mudar status)
class ConsultaSetStatusView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "consultas.change_consulta"
    success_url = reverse_lazy("consultas:list")

    def post(self, request, pk, status_code):
        consulta = get_object_or_404(Consulta, pk=pk)
        if status_code not in dict(Consulta.Status.choices):
            messages.error(request, "Status inválido.")
            return redirect(self.success_url)
        consulta.status = status_code
        consulta.save(update_fields=["status"])
        messages.success(request, "Status da consulta atualizado.")
        return redirect(self.success_url)

# LEMBRETES
class LembreteCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Lembrete
    form_class = LembreteForm
    template_name = "consultas/lembrete_form.html"
    permission_required = "consultas.add_lembrete"

    def get_initial(self):
        initial = super().get_initial()
        if "consulta" in self.request.GET:
            initial["consulta"] = self.request.GET.get("consulta")
        return initial

    def get_success_url(self):
        messages.success(self.request, "Lembrete agendado.")
        return reverse_lazy("consultas:detail", kwargs={"pk": self.object.consulta_id})
