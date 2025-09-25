# consultas/urls.py
from django.urls import path
from . import views

app_name = "consultas"

urlpatterns = [
    path("", views.ConsultaListView.as_view(), name="list"),
    path("<int:pk>/", views.ConsultaDetailView.as_view(), name="detail"),
    path("nova/", views.ConsultaCreateView.as_view(), name="create"),
    path("<int:pk>/editar/", views.ConsultaUpdateView.as_view(), name="update"),
    path("<int:pk>/excluir/", views.ConsultaDeleteView.as_view(), name="delete"),
    path("<int:pk>/status/<str:status_code>/", views.ConsultaSetStatusView.as_view(), name="set_status"),
    path("lembrete/novo/", views.LembreteCreateView.as_view(), name="lembrete_create"),
]
