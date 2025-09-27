# pacientes/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Paciente
from .forms import PacienteForm


class PacienteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Paciente
    template_name = "pacientes/paciente_list.html"
    context_object_name = "pacientes"
    paginate_by = 20
    permission_required = "pacientes.view_paciente"

    def get_queryset(self):
        # Apenas pacientes ativos
        qs = Paciente.objects.filter(is_active=True)
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(nome__icontains=q) | Q(cpf__icontains=q) | Q(email__icontains=q))
        return qs.order_by("nome")


class PacienteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Paciente
    template_name = "pacientes/paciente_detail.html"
    context_object_name = "paciente"
    permission_required = "pacientes.view_paciente"

    def get_queryset(self):
        # Impede acessar detalhes de paciente arquivado
        return Paciente.objects.filter(is_active=True)


class PacienteCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "pacientes/paciente_form.html"
    permission_required = "pacientes.add_paciente"
    success_url = reverse_lazy("pacientes:list")

    def form_valid(self, form):
        messages.success(self.request, "Paciente cadastrado.")
        return super().form_valid(form)


class PacienteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "pacientes/paciente_form.html"
    permission_required = "pacientes.change_paciente"
    success_url = reverse_lazy("pacientes:list")

    def get_queryset(self):
        # Editar apenas ativos
        return Paciente.objects.filter(is_active=True)

    def form_valid(self, form):
        messages.success(self.request, "Paciente atualizado.")
        return super().form_valid(form)


class PacienteDisableView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Paciente
    template_name = "pacientes/paciente_confirm_delete.html"
    permission_required = "pacientes.delete_paciente"
    success_url = reverse_lazy("pacientes:list")

    def get_queryset(self):
        return Paciente.objects.filter(is_active=True)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Paciente arquivado com sucesso.")
        return super().delete(request, *args, **kwargs)


class PacienteArchivedListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Paciente
    template_name = "pacientes/paciente_archived_list.html"
    context_object_name = "pacientes"
    paginate_by = 20
    permission_required = "pacientes.view_paciente"

    def get_queryset(self):
        qs = Paciente.objects.filter(is_active=False)
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(nome__icontains=q) | Q(cpf__icontains=q) | Q(email__icontains=q))
        return qs.order_by("nome")


class PacienteReactivateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "pacientes.change_paciente"

    def post(self, request, pk):
        paciente = get_object_or_404(Paciente, pk=pk, is_active=False)
        paciente.is_active = True
        paciente.deleted_at = None
        paciente.save(update_fields=["is_active", "deleted_at"])
        messages.success(request, "Paciente reativado com sucesso.")
        # volta para a lista de arquivados (ou use 'pacientes:list' se preferir)
        return redirect(reverse_lazy("pacientes:archived_list"))