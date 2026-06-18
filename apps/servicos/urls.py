from django.urls import path

from .views import (
    ServicoListView,
    ServicoCreateView,
    ServicoUpdateView,
    servico_delete
)

urlpatterns = [
    path(
        '',
        ServicoListView.as_view(),
        name='servico-list'
    ),

    path(
        'novo/',
        ServicoCreateView.as_view(),
        name='servico-create'
    ),

    path(
        '<int:pk>/editar/',
        ServicoUpdateView.as_view(),
        name='servico-update'
    ),

    path(
        '<int:pk>/excluir/',
        servico_delete,
        name='servico-delete'
    ),
]
