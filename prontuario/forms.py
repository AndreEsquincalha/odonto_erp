# prontuario/forms.py
from django import forms
from .models import Odontograma, EvolucaoClinica, Anexo, Receita, TermoConsentimento

class OdontogramaForm(forms.ModelForm):
    class Meta:
        model = Odontograma
        fields = ["paciente", "dente", "superficie", "condicao", "procedimento_executado"]

class EvolucaoForm(forms.ModelForm):
    class Meta:
        model = EvolucaoClinica
        fields = ["consulta", "usuario", "anotacao"]

class AnexoForm(forms.ModelForm):
    class Meta:
        model = Anexo
        fields = ["paciente", "consulta", "caminho_arquivo", "tipo_arquivo"]

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ["consulta", "texto"]

class TermoConsentimentoForm(forms.ModelForm):
    class Meta:
        model = TermoConsentimento
        fields = ["paciente", "procedimento", "texto", "assinado_em", "caminho_assinatura"]
        widgets = {"assinado_em": forms.DateTimeInput(attrs={"type": "datetime-local"})}
