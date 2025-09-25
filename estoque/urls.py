# estoque/urls.py
from django.urls import path
from . import views
app_name = "estoque"

urlpatterns = [
    path("itens/", views.ItemEstoqueListView.as_view(), name="item_list"),
    path("itens/novo/", views.ItemEstoqueCreateView.as_view(), name="item_create"),
    path("itens/<int:pk>/editar/", views.ItemEstoqueUpdateView.as_view(), name="item_update"),
    path("movimento/novo/", views.MovimentoEstoqueCreateView.as_view(), name="movimento_create"),
]
