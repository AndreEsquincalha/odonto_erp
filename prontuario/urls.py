# prontuario/urls.py
from django.urls import path
from . import views
app_name = "prontuario"

urlpatterns = [
    path("odontograma/", views.OdontogramaListView.as_view(), name="odontograma_list"),
    path("odontograma/novo/", views.OdontogramaCreateView.as_view(), name="odontograma_create"),
    path("odontograma/<int:pk>/editar/", views.OdontogramaUpdateView.as_view(), name="odontograma_update"),
    path("odontograma/<int:pk>/excluir/", views.OdontogramaDeleteView.as_view(), name="odontograma_delete"),

    path("evolucao/nova/", views.EvolucaoCreateView.as_view(), name="evolucao_create"),
    path("anexo/novo/", views.AnexoCreateView.as_view(), name="anexo_create"),
    path("receita/nova/", views.ReceitaCreateView.as_view(), name="receita_create"),

    path("termos/", views.TermoConsentimentoListView.as_view(), name="termo_list"),
    path("termos/novo/", views.TermoConsentimentoCreateView.as_view(), name="termo_create"),
]
