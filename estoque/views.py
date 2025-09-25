# estoque/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import ItemEstoque, MovimentoEstoque
from .forms import ItemEstoqueForm, MovimentoEstoqueForm

class ItemEstoqueListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ItemEstoque
    template_name = "estoque/item_list.html"
    context_object_name = "itens"
    paginate_by = 30
    permission_required = "estoque.view_itemestoque"

class ItemEstoqueCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ItemEstoque
    form_class = ItemEstoqueForm
    template_name = "estoque/item_form.html"
    permission_required = "estoque.add_itemestoque"
    success_url = reverse_lazy("estoque:item_list")

class ItemEstoqueUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ItemEstoque
    form_class = ItemEstoqueForm
    template_name = "estoque/item_form.html"
    permission_required = "estoque.change_itemestoque"
    success_url = reverse_lazy("estoque:item_list")

class MovimentoEstoqueCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MovimentoEstoque
    form_class = MovimentoEstoqueForm
    template_name = "estoque/movimento_form.html"
    permission_required = "estoque.add_movimentoestoque"
    success_url = reverse_lazy("estoque:item_list")

    def form_valid(self, form):
        messages.success(self.request, "Movimento registrado.")
        return super().form_valid(form)
