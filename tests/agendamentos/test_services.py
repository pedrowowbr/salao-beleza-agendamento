from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from apps.agendamentos.models import Agendamento, StatusAgendamento
from apps.agendamentos.services.agendamento_service import AgendamentoService
from apps.clientes.models import Cliente


def data_na_semana(semanas_a_frente, dia_da_semana, hora=10):
    """
    dia_da_semana: 0 (segunda) a 6 (domingo).
    Garante que duas datas com o mesmo `semanas_a_frente` caiam sempre
    na mesma semana, independente do dia em que o teste é executado.
    """
    hoje = timezone.localdate()
    inicio_semana_atual = hoje - timedelta(days=hoje.weekday())
    dia = inicio_semana_atual + \
        timedelta(weeks=semanas_a_frente, days=dia_da_semana)
    return timezone.make_aware(datetime.combine(dia, datetime.min.time()) + timedelta(hours=hora))


class PodeAlterarTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='maria', password='123456')
        self.cliente = Cliente.objects.create(
            user=user, nome='Maria', email='maria@example.com',
            telefone='14999990000', endereco='Rua A, 123'
        )

    def _criar_agendamento(self, data_hora):
        return Agendamento.objects.create(cliente=self.cliente, data_hora=data_hora)

    def test_nao_pode_alterar_agendamento_em_menos_de_2_dias(self):
        agendamento = self._criar_agendamento(
            timezone.now() + timedelta(hours=10))
        self.assertFalse(AgendamentoService.pode_alterar(agendamento))

    def test_pode_alterar_agendamento_com_mais_de_2_dias(self):
        agendamento = self._criar_agendamento(
            timezone.now() + timedelta(days=5))
        self.assertTrue(AgendamentoService.pode_alterar(agendamento))

    def test_nao_pode_alterar_agendamento_ja_passado(self):
        agendamento = self._criar_agendamento(
            timezone.now() - timedelta(days=1))
        self.assertFalse(AgendamentoService.pode_alterar(agendamento))


class BuscarAgendamentoMesmaSemanaTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='joao', password='123456')
        self.cliente = Cliente.objects.create(
            user=user, nome='João', email='joao@example.com',
            telefone='14999991111', endereco='Rua B, 456'
        )

    def test_encontra_agendamento_na_mesma_semana(self):
        primeira_data = data_na_semana(semanas_a_frente=2, dia_da_semana=1)
        segunda_data = data_na_semana(semanas_a_frente=2, dia_da_semana=4)

        Agendamento.objects.create(
            cliente=self.cliente, data_hora=primeira_data)

        encontrado = AgendamentoService.buscar_agendamento_mesma_semana(
            self.cliente, segunda_data)
        self.assertIsNotNone(encontrado)

    def test_nao_encontra_agendamento_em_semana_diferente(self):
        primeira_data = data_na_semana(semanas_a_frente=2, dia_da_semana=1)
        outra_semana = data_na_semana(semanas_a_frente=3, dia_da_semana=1)

        Agendamento.objects.create(
            cliente=self.cliente, data_hora=primeira_data)

        encontrado = AgendamentoService.buscar_agendamento_mesma_semana(
            self.cliente, outra_semana)
        self.assertIsNone(encontrado)

    def test_ignora_agendamento_cancelado(self):
        primeira_data = data_na_semana(semanas_a_frente=2, dia_da_semana=1)

        Agendamento.objects.create(
            cliente=self.cliente, data_hora=primeira_data, status=StatusAgendamento.CANCELADO
        )

        encontrado = AgendamentoService.buscar_agendamento_mesma_semana(
            self.cliente, primeira_data)
        self.assertIsNone(encontrado)
