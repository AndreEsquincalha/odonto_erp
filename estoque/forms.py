# estoque/forms.py
from django import forms
from .models import ItemEstoque, MovimentoEstoque

class ItemEstoqueForm(forms.ModelForm):
    class Meta:
        model = ItemEstoque
        fields = ["descricao", "marca", "lote", "validade", "qtd_minima", "qtd_atual"]
        widgets = {"validade": forms.DateInput(attrs={"type": "date"})}

class MovimentoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentoEstoque
        fields = ["item", "tipo_movimento", "quantidade", "motivo", "consulta"]
