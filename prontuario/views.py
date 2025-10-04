# prontuario/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Odontograma, EvolucaoClinica, Anexo, Receita, TermoConsentimento
from .forms import OdontogramaForm, EvolucaoForm, AnexoForm, ReceitaForm, TermoConsentimentoForm

class OdontogramaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Odontograma
    template_name = "prontuario/odontograma_list.html"
    context_object_name = "odontogramas"
    paginate_by = 30
    permission_required = "prontuario.view_odontograma"

    def get_queryset(self):
        qs = super().get_queryset().select_related("paciente")
        pid = self.request.GET.get("paciente")
        if pid:
            qs = qs.filter(paciente_id=pid)
        return qs.order_by("paciente__nome", "dente", "superficie", "-criado_em")

class OdontogramaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Odontograma
    form_class = OdontogramaForm
    template_name = "prontuario/odontograma_form.html"
    permission_required = "prontuario.add_odontograma"
    success_url = reverse_lazy("prontuario:odontograma_list")

    def form_valid(self, form):
        messages.success(self.request, "Registro de odontograma criado.")
        return super().form_valid(form)

class OdontogramaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Odontograma
    form_class = OdontogramaForm
    template_name = "prontuario/odontograma_form.html"
    permission_required = "prontuario.change_odontograma"
    success_url = reverse_lazy("prontuario:odontograma_list")

class OdontogramaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Odontograma
    template_name = "prontuario/odontograma_confirm_delete.html"
    permission_required = "prontuario.delete_odontograma"
    success_url = reverse_lazy("prontuario:odontograma_list")

# Evolução
class EvolucaoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = EvolucaoClinica
    form_class = EvolucaoForm
    template_name = "prontuario/evolucao_form.html"
    permission_required = "prontuario.add_evolucaoclinica"

    def get_success_url(self):
        messages.success(self.request, "Evolução registrada.")
        return reverse_lazy("consultas:detail", kwargs={"pk": self.object.consulta_id})

# Anexo
class AnexoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Anexo
    form_class = AnexoForm
    template_name = "prontuario/anexo_form.html"
    permission_required = "prontuario.add_anexo"

    def get_success_url(self):
        messages.success(self.request, "Anexo salvo.")
        return reverse_lazy("consultas:detail", kwargs={"pk": self.object.consulta_id})

# Receita
class ReceitaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Receita
    form_class = ReceitaForm
    template_name = "prontuario/receita_form.html"
    permission_required = "prontuario.add_receita"

    def get_success_url(self):
        messages.success(self.request, "Receita emitida.")
        return reverse_lazy("consultas:detail", kwargs={"pk": self.object.consulta_id})

# Termo
class TermoConsentimentoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = TermoConsentimento
    form_class = TermoConsentimentoForm
    template_name = "prontuario/termo_form.html"
    permission_required = "prontuario.add_termoconsentimento"
    success_url = reverse_lazy("prontuario:termo_list")

class TermoConsentimentoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = TermoConsentimento
    template_name = "prontuario/termo_list.html"
    context_object_name = "termos"
    permission_required = "prontuario.view_termoconsentimento"

    def get_queryset(self):
        qs = super().get_queryset().select_related("paciente", "procedimento")
        pid = self.request.GET.get("paciente")
        if pid:
            qs = qs.filter(paciente_id=pid)
        return qs.order_by("-assinado_em", "paciente__nome")
