# pacientes/urls.py
from django.urls import path
from . import views
app_name = "pacientes"

urlpatterns = [
    path("", views.PacienteListView.as_view(), name="list"),
    path("novo/", views.PacienteCreateView.as_view(), name="create"),
    path("<int:pk>/", views.PacienteDetailView.as_view(), name="detail"),
    path("<int:pk>/editar/", views.PacienteUpdateView.as_view(), name="update"),
    path("<int:pk>/arquivar/", views.PacienteDisableView.as_view(), name="delete"),
    path("arquivados/", views.PacienteArchivedListView.as_view(), name="archived_list"),
    path("<int:pk>/reativar/", views.PacienteReactivateView.as_view(), name="reactivate"),
]
