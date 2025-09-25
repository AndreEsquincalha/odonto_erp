# pacientes/forms.py
from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ["nome", "cpf", "data_nascimento", "telefone", "email", "endereco"]
        widgets = {"data_nascimento": forms.DateInput(attrs={"type": "date"})}
