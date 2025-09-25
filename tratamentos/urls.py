# tratamentos/urls.py
from django.urls import path
from . import views
app_name = "tratamentos"

urlpatterns = [
    path("planos/", views.PlanoListView.as_view(), name="plano_list"),
    path("planos/novo/", views.PlanoCreateView.as_view(), name="plano_create"),
    path("planos/<int:pk>/", views.PlanoDetailView.as_view(), name="plano_detail"),
    path("planos/<int:pk>/editar/", views.PlanoUpdateView.as_view(), name="plano_update"),
    path("planos/<int:pk>/excluir/", views.PlanoDeleteView.as_view(), name="plano_delete"),

    path("catalogo/", views.ProcedimentoCatalogoListView.as_view(), name="catalogo_list"),
    path("catalogo/novo/", views.ProcedimentoCatalogoCreateView.as_view(), name="catalogo_create"),
    path("catalogo/<int:pk>/editar/", views.ProcedimentoCatalogoUpdateView.as_view(), name="catalogo_update"),
    path("catalogo/<int:pk>/excluir/", views.ProcedimentoCatalogoDeleteView.as_view(), name="catalogo_delete"),

    path("planejado/novo/", views.ProcedimentoPlanejadoCreateView.as_view(), name="planejado_create"),
    path("planejado/<int:pk>/editar/", views.ProcedimentoPlanejadoUpdateView.as_view(), name="planejado_update"),
    path("planejado/<int:pk>/excluir/", views.ProcedimentoPlanejadoDeleteView.as_view(), name="planejado_delete"),

    path("executado/novo/", views.ProcedimentoExecutadoCreateView.as_view(), name="executado_create"),
]
