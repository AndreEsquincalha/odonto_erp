# tratamentos/forms.py
from django import forms
from .models import PlanoTratamento, CatalogoProcedimento, ProcedimentoPlanejado, ProcedimentoExecutado

class PlanoTratamentoForm(forms.ModelForm):
    class Meta:
        model = PlanoTratamento
        fields = ["paciente", "status"]

class CatalogoProcedimentoForm(forms.ModelForm):
    class Meta:
        model = CatalogoProcedimento
        fields = ["codigo", "nome", "duracao_min", "preco_base"]

class ProcedimentoPlanejadoForm(forms.ModelForm):
    class Meta:
        model = ProcedimentoPlanejado
        fields = ["plano", "procedimento", "dente_superficie", "quantidade", "valor_unitario", "status"]

class ProcedimentoExecutadoForm(forms.ModelForm):
    class Meta:
        model = ProcedimentoExecutado
        fields = ["consulta", "planejado", "procedimento", "dente", "superficie", "quantidade", "valor_unitario", "observacoes"]
