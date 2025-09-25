from django.db import models
from django.conf import settings
from pacientes.models import Paciente
from consultas.models import Consulta
from tratamentos.models import CatalogoProcedimento, ProcedimentoExecutado

class Odontograma(models.Model):
    class Dente(models.TextChoices):
        # Permanentes - Superior Direito
        D11 = "11", "11 - Incisivo Central Superior Direito"
        D12 = "12", "12 - Incisivo Lateral Superior Direito"
        D13 = "13", "13 - Canino Superior Direito"
        D14 = "14", "14 - 1º Pré-molar Superior Direito"
        D15 = "15", "15 - 2º Pré-molar Superior Direito"
        D16 = "16", "16 - 1º Molar Superior Direito"
        D17 = "17", "17 - 2º Molar Superior Direito"
        D18 = "18", "18 - 3º Molar Superior Direito"

        # Permanentes - Superior Esquerdo
        D21 = "21", "21 - Incisivo Central Superior Esquerdo"
        D22 = "22", "22 - Incisivo Lateral Superior Esquerdo"
        D23 = "23", "23 - Canino Superior Esquerdo"
        D24 = "24", "24 - 1º Pré-molar Superior Esquerdo"
        D25 = "25", "25 - 2º Pré-molar Superior Esquerdo"
        D26 = "26", "26 - 1º Molar Superior Esquerdo"
        D27 = "27", "27 - 2º Molar Superior Esquerdo"
        D28 = "28", "28 - 3º Molar Superior Esquerdo"

        # Permanentes - Inferior Esquerdo
        D31 = "31", "31 - Incisivo Central Inferior Esquerdo"
        D32 = "32", "32 - Incisivo Lateral Inferior Esquerdo"
        D33 = "33", "33 - Canino Inferior Esquerdo"
        D34 = "34", "34 - 1º Pré-molar Inferior Esquerdo"
        D35 = "35", "35 - 2º Pré-molar Inferior Esquerdo"
        D36 = "36", "36 - 1º Molar Inferior Esquerdo"
        D37 = "37", "37 - 2º Molar Inferior Esquerdo"
        D38 = "38", "38 - 3º Molar Inferior Esquerdo"

        # Permanentes - Inferior Direito
        D41 = "41", "41 - Incisivo Central Inferior Direito"
        D42 = "42", "42 - Incisivo Lateral Inferior Direito"
        D43 = "43", "43 - Canino Inferior Direito"
        D44 = "44", "44 - 1º Pré-molar Inferior Direito"
        D45 = "45", "45 - 2º Pré-molar Inferior Direito"
        D46 = "46", "46 - 1º Molar Inferior Direito"
        D47 = "47", "47 - 2º Molar Inferior Direito"
        D48 = "48", "48 - 3º Molar Inferior Direito"

        # Decíduos - Superior Direito
        D51 = "51", "51 - Incisivo Central Superior Direito (decíduo)"
        D52 = "52", "52 - Incisivo Lateral Superior Direito (decíduo)"
        D53 = "53", "53 - Canino Superior Direito (decíduo)"
        D54 = "54", "54 - 1º Molar Superior Direito (decíduo)"
        D55 = "55", "55 - 2º Molar Superior Direito (decíduo)"

        # Decíduos - Superior Esquerdo
        D61 = "61", "61 - Incisivo Central Superior Esquerdo (decíduo)"
        D62 = "62", "62 - Incisivo Lateral Superior Esquerdo (decíduo)"
        D63 = "63", "63 - Canino Superior Esquerdo (decíduo)"
        D64 = "64", "64 - 1º Molar Superior Esquerdo (decíduo)"
        D65 = "65", "65 - 2º Molar Superior Esquerdo (decíduo)"

        # Decíduos - Inferior Esquerdo
        D71 = "71", "71 - Incisivo Central Inferior Esquerdo (decíduo)"
        D72 = "72", "72 - Incisivo Lateral Inferior Esquerdo (decíduo)"
        D73 = "73", "73 - Canino Inferior Esquerdo (decíduo)"
        D74 = "74", "74 - 1º Molar Inferior Esquerdo (decíduo)"
        D75 = "75", "75 - 2º Molar Inferior Esquerdo (decíduo)"

        # Decíduos - Inferior Direito
        D81 = "81", "81 - Incisivo Central Inferior Direito (decíduo)"
        D82 = "82", "82 - Incisivo Lateral Inferior Direito (decíduo)"
        D83 = "83", "83 - Canino Inferior Direito (decíduo)"
        D84 = "84", "84 - 1º Molar Inferior Direito (decíduo)"
        D85 = "85", "85 - 2º Molar Inferior Direito (decíduo)"
    
    class Superficie(models.TextChoices):
        M = "M", "Mesial"
        D = "D", "Distal"
        O = "O", "Oclusal"
        I = "I", "Incisal"
        V = "V", "Vestibular/Bucal"
        P = "P", "Palatina"
        L = "L", "Lingual"

    paciente = models.ForeignKey(
        Paciente, 
        verbose_name=("Paciente"), 
        on_delete=models.PROTECT
    )
    dente = models.CharField(max_length=2, choices=Dente.choices)
    superficie = models.CharField(
        max_length=1,
        choices=Superficie.choices,
        blank=True
    )
    condicao = models.CharField(max_length=100)
    procedimento_executado = models.ForeignKey(
        ProcedimentoExecutado, on_delete=models.SET_NULL, null=True, blank=True, related_name="alteracoes_odontograma"
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["paciente", "dente"]
        verbose_name = "Odontograma"
        verbose_name_plural = "Odontogramas"

    def __str__(self):
        if self.superficie:
            return f"{self.paciente.nome} - Dente {self.dente} ({self.get_superficie_display()}): {self.condicao}"
        return f"{self.paciente.nome} - Dente {self.dente}: {self.condicao}"


class EvolucaoClinica(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name="evolucoes")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="evolucoes_clinicas")
    anotacao = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Evolução Clínica"
        verbose_name_plural = "Evoluções Clínicas"

    def __str__(self):
        return f"Evolução {self.consulta.paciente.nome} ({self.criado_em:%d/%m/%Y %H:%M})"


class Anexo(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name="anexos")
    consulta = models.ForeignKey(Consulta, on_delete=models.PROTECT, related_name="anexos")
    caminho_arquivo = models.CharField(max_length=300)
    tipo_arquivo = models.CharField(max_length=50, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Anexo"
        verbose_name_plural = "Anexos"

    def __str__(self):
        return f"Anexo: {self.caminho_arquivo}"


class Receita(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.PROTECT, related_name="receitas")
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Receita"
        verbose_name_plural = "Receitas"

    def __str__(self):
        return f"Receita de {self.consulta.paciente.nome} ({self.criado_em:%d/%m/%Y})"


class TermoConsentimento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name="termos_consentimento")
    procedimento = models.ForeignKey(CatalogoProcedimento, on_delete=models.PROTECT, related_name="termos")
    texto = models.TextField()
    assinado_em = models.DateTimeField(null=True, blank=True)
    caminho_assinatura = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ["-assinado_em"]
        verbose_name = "Termo de Consentimento"
        verbose_name_plural = "Termos de Consentimento"

    def __str__(self):
        return f"Termo de {self.paciente.nome} - {self.procedimento.nome}"