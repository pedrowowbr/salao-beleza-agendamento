from django.urls import path

from .views import (
    AgendamentoListView,
    AgendamentoCreateView,
    AgendamentoUpdateView,
    AgendamentoDetailView,
    alterar_status_agendamento,
    confirmar_agendamento,
    cancelar_agendamento,
    agendamento_delete
)

urlpatterns = [
    path(
        '',
        AgendamentoListView.as_view(),
        name='agendamento-list'
    ),

    path(
        'novo/',
        AgendamentoCreateView.as_view(),
        name='agendamento-create'
    ),

    path(
        '<int:pk>/',
        AgendamentoDetailView.as_view(),
        name='agendamento-detail'
    ),

    path(
        '<int:pk>/editar/',
        AgendamentoUpdateView.as_view(),
        name='agendamento-update'
    ),

    path(
        '<int:pk>/excluir/',
        agendamento_delete,
        name='agendamento-delete'
    ),

    path(
        '<int:pk>/status/',
        alterar_status_agendamento,
        name='agendamento-status'
    ),

    path(
        '<int:pk>/confirmar/',
        confirmar_agendamento,
        name='agendamento-confirmar'
    ),

    path(
        '<int:pk>/cancelar/',
        cancelar_agendamento,
        name='agendamento-cancelar'
    ),
]
