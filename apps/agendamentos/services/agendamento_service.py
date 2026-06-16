from datetime import timedelta
from django.utils import timezone
from apps.agendamentos.models import Agendamento


class AgendamentoService:
    @staticmethod
    def pode_alterar(agendamento):
        """
        Permite alteração apenas se faltar mais de 2 dias.
        """

        limite = timezone.now() + timedelta(days=2)

        return agendamento.data_hora > limite

    @staticmethod
    def buscar_agendamento_mesma_semana(cliente, data_agendamento):
        """
        Busca se o cliente já possui um agendamento
        na mesma semana.
        """

        inicio_semana = (
            data_agendamento.date()
            - timedelta(days=data_agendamento.weekday())
        )

        fim_semana = inicio_semana + timedelta(days=6)

        return (
            Agendamento.objects
            .filter(
                cliente=cliente,
                data_hora__date__range=(
                    inicio_semana,
                    fim_semana
                )
            )
            .exclude(status='CANCELADO')
            .first()
        )

    @staticmethod
    def confirmar_agendamento(agendamento):
        """
        Confirma um agendamento.
        """

        agendamento.status = 'CONFIRMADO'
        agendamento.save(
            update_fields=['status']
        )

        return agendamento

    @staticmethod
    def cancelar_agendamento(agendamento):
        """
        Cancela um agendamento.
        """

        agendamento.status = 'CANCELADO'
        agendamento.save(
            update_fields=['status']
        )

        return agendamento
