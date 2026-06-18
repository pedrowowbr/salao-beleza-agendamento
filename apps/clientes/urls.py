from django.urls import path

from .views import (
    ClienteListView,
    ClienteCreateView,
    ClienteUpdateView,
    cliente_delete
)

urlpatterns = [
    path(
        '',
        ClienteListView.as_view(),
        name='cliente-list'
    ),

    path(
        'novo/',
        ClienteCreateView.as_view(),
        name='cliente-create'
    ),

    path(
        '<int:pk>/editar/',
        ClienteUpdateView.as_view(),
        name='cliente-update'
    ),

    path(
        '<int:pk>/excluir/',
        cliente_delete,
        name='cliente-delete'
    ),
]
