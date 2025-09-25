# financeiro/forms.py
from django import forms
from .models import Fatura, Pagamento

class FaturaForm(forms.ModelForm):
    class Meta:
        model = Fatura
        fields = ["paciente", "origem", "valor", "status", "numero_nfse"]

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ["fatura", "metodo_pagamento", "valor", "parcela"]
