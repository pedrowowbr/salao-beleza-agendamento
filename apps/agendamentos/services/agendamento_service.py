from datetime import timedelta
from django.utils import timezone
from apps.agendamentos.models import (
    Agendamento,
    StatusAgendamento
)


class AgendamentoService:
    @staticmethod
    def pode_alterar(agendamento):

        limite = timezone.now() + timedelta(days=2)

        return agendamento.data_hora > limite

    @staticmethod
    def buscar_agendamento_mesma_semana(
        cliente,
        data_hora
    ):

        inicio_semana = (
            data_hora.date()
            - timedelta(days=data_hora.weekday())
        )

        fim_semana = (
            inicio_semana
            + timedelta(days=6)
        )

        return (
            Agendamento.objects
            .filter(
                cliente=cliente,
                data_hora__date__range=(
                    inicio_semana,
                    fim_semana
                )
            )
            .exclude(
                status=StatusAgendamento.CANCELADO
            )
            .first()
        )

    @staticmethod
    def confirmar_agendamento(
        agendamento
    ):

        agendamento.status = (
            StatusAgendamento.CONFIRMADO
        )

        agendamento.save()

        return agendamento

    @staticmethod
    def cancelar_agendamento(
        agendamento
    ):

        agendamento.status = (
            StatusAgendamento.CANCELADO
        )

        agendamento.save()

        return agendamento
