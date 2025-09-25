# pacientes/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Paciente
from .forms import PacienteForm

class PacienteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Paciente
    template_name = "pacientes/paciente_list.html"
    context_object_name = "pacientes"
    paginate_by = 20
    permission_required = "pacientes.view_paciente"

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            from django.db.models import Q
            qs = qs.filter(Q(nome__icontains=q) | Q(cpf__icontains=q) | Q(email__icontains=q))
        return qs.order_by("nome")

class PacienteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Paciente
    template_name = "pacientes/paciente_detail.html"
    context_object_name = "paciente"
    permission_required = "pacientes.view_paciente"

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

    def form_valid(self, form):
        messages.success(self.request, "Paciente atualizado.")
        return super().form_valid(form)

class PacienteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Paciente
    template_name = "pacientes/paciente_confirm_delete.html"
    permission_required = "pacientes.delete_paciente"
    success_url = reverse_lazy("pacientes:list")
