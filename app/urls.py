# app/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path("pacientes/", include("pacientes.urls")),
    path("consultas/", include("consultas.urls")),
    path("prontuario/", include("prontuario.urls")),
    path("tratamentos/", include("tratamentos.urls")),
    path("financeiro/", include("financeiro.urls")),
    path("estoque/", include("estoque.urls")),
]
