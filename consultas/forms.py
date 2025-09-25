# consultas/forms.py
from django import forms
from .models import Consulta, Lembrete

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ["paciente", "status", "inicio", "fim", "sala", "observacoes"]
        widgets = {
            "inicio": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "fim": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

class LembreteForm(forms.ModelForm):
    class Meta:
        model = Lembrete
        fields = ["consulta", "canal", "agendado_em", "status"]
        widgets = {"agendado_em": forms.DateTimeInput(attrs={"type": "datetime-local"})}
