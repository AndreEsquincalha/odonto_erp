# tratamentos/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.forms import inlineformset_factory
from .models import PlanoTratamento, CatalogoProcedimento, ProcedimentoPlanejado, ProcedimentoExecutado
from .forms import PlanoTratamentoForm, CatalogoProcedimentoForm, ProcedimentoPlanejadoForm, ProcedimentoExecutadoForm
from pacientes.models import Paciente

class PlanoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = PlanoTratamento
    template_name = "tratamentos/plano_list.html"
    context_object_name = "planos"
    paginate_by = 20
    permission_required = "tratamentos.view_planotratamento"

    def get_queryset(self):
        qs = super().get_queryset().select_related("paciente")

        pid = self.request.GET.get("paciente")
        if pid:
            qs = qs.filter(paciente_id=pid)

        status = self.request.GET.get("status")
        valid = {code for code, _ in PlanoTratamento.Status.choices}
        if status in valid:
            qs = qs.filter(status=status)

        return qs
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["pacientes"] = Paciente.objects.only("id", "nome").order_by("nome")
        ctx["current_status"] = self.request.GET.get("status", "")
        ctx["current_paciente"] = self.request.GET.get("paciente", "")
        return ctx


class PlanoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = PlanoTratamento
    template_name = "tratamentos/plano_detail.html"
    context_object_name = "plano"
    permission_required = "tratamentos.view_planotratamento"

class PlanoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = PlanoTratamento
    form_class = PlanoTratamentoForm
    template_name = "tratamentos/plano_form.html"
    permission_required = "tratamentos.add_planotratamento"
    success_url = reverse_lazy("tratamentos:plano_list")

    def form_valid(self, form):
        messages.success(self.request, "Plano criado.")
        return super().form_valid(form)

class PlanoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = PlanoTratamento
    form_class = PlanoTratamentoForm
    template_name = "tratamentos/plano_form.html"
    permission_required = "tratamentos.change_planotratamento"
    success_url = reverse_lazy("tratamentos:plano_list")

class PlanoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = PlanoTratamento
    template_name = "tratamentos/plano_confirm_delete.html"
    permission_required = "tratamentos.delete_planotratamento"
    success_url = reverse_lazy("tratamentos:plano_list")

# Catálogo
class ProcedimentoCatalogoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CatalogoProcedimento
    template_name = "tratamentos/catalogo_list.html"
    context_object_name = "procedimentos"
    permission_required = "tratamentos.view_catalogoprocedimento"

class ProcedimentoCatalogoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CatalogoProcedimento
    form_class = CatalogoProcedimentoForm
    template_name = "tratamentos/catalogo_form.html"
    permission_required = "tratamentos.add_catalogoprocedimento"
    success_url = reverse_lazy("tratamentos:catalogo_list")

class ProcedimentoCatalogoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CatalogoProcedimento
    form_class = CatalogoProcedimentoForm
    template_name = "tratamentos/catalogo_form.html"
    permission_required = "tratamentos.change_catalogoprocedimento"
    success_url = reverse_lazy("tratamentos:catalogo_list")

class ProcedimentoCatalogoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CatalogoProcedimento
    template_name = "tratamentos/catalogo_confirm_delete.html"
    permission_required = "tratamentos.delete_catalogoprocedimento"
    success_url = reverse_lazy("tratamentos:catalogo_list")

# Planejados
class ProcedimentoPlanejadoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ProcedimentoPlanejado
    form_class = ProcedimentoPlanejadoForm
    template_name = "tratamentos/planejado_form.html"
    permission_required = "tratamentos.add_procedimentoplanejado"

    def get_success_url(self):
        messages.success(self.request, "Procedimento planejado adicionado.")
        return reverse_lazy("tratamentos:plano_detail", kwargs={"pk": self.object.plano_id})

class ProcedimentoPlanejadoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ProcedimentoPlanejado
    form_class = ProcedimentoPlanejadoForm
    template_name = "tratamentos/planejado_form.html"
    permission_required = "tratamentos.change_procedimentoplanejado"

    def get_success_url(self):
        messages.success(self.request, "Procedimento planejado atualizado.")
        return reverse_lazy("tratamentos:plano_detail", kwargs={"pk": self.object.plano_id})

class ProcedimentoPlanejadoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ProcedimentoPlanejado
    template_name = "tratamentos/planejado_confirm_delete.html"
    permission_required = "tratamentos.delete_procedimentoplanejado"

    def get_success_url(self):
        messages.success(self.request, "Procedimento planejado removido.")
        return reverse_lazy("tratamentos:plano_detail", kwargs={"pk": self.object.plano_id})

# Executados
class ProcedimentoExecutadoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ProcedimentoExecutado
    form_class = ProcedimentoExecutadoForm
    template_name = "tratamentos/executado_form.html"
    permission_required = "tratamentos.add_procedimentoexecutado"

    def get_initial(self):
        initial = super().get_initial()
        if "consulta" in self.request.GET:
            initial["consulta"] = self.request.GET.get("consulta")
        if "planejado" in self.request.GET:
            initial["planejado"] = self.request.GET.get("planejado")
        return initial

    def get_success_url(self):
        messages.success(self.request, "Procedimento executado registrado.")
        return reverse_lazy("consultas:detail", kwargs={"pk": self.object.consulta_id})
