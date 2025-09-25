# financeiro/urls.py
from django.urls import path
from . import views
app_name = "financeiro"

urlpatterns = [
    path("faturas/", views.FaturaListView.as_view(), name="fatura_list"),
    path("faturas/nova/", views.FaturaCreateView.as_view(), name="fatura_create"),
    path("faturas/<int:pk>/", views.FaturaDetailView.as_view(), name="fatura_detail"),
    path("faturas/<int:pk>/editar/", views.FaturaUpdateView.as_view(), name="fatura_update"),
    path("pagamentos/novo/", views.PagamentoCreateView.as_view(), name="pagamento_create"),
]
