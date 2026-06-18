from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.agendamentos.models import Agendamento, StatusAgendamento
from apps.clientes.models import Cliente


def criar_cliente(username, telefone):
    user = User.objects.create_user(username=username, password='123456')
    return Cliente.objects.create(
        user=user,
        nome=username,
        email=f'{username}@example.com',
        telefone=telefone,
        endereco='Rua Teste, 1'
    )


class AgendamentoListViewTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username='staff', password='123456', is_staff=True)
        self.cliente1 = criar_cliente('cliente1', '14911110000')
        self.cliente2 = criar_cliente('cliente2', '14911110001')

        self.agendamento1 = Agendamento.objects.create(
            cliente=self.cliente1, data_hora=timezone.now() + timedelta(days=5)
        )
        self.agendamento2 = Agendamento.objects.create(
            cliente=self.cliente2, data_hora=timezone.now() + timedelta(days=5)
        )

    def test_redireciona_usuario_nao_logado(self):
        response = self.client.get(reverse('agendamento-list'))
        self.assertEqual(response.status_code, 302)

    def test_staff_ve_todos_os_agendamentos(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse('agendamento-list'))
        self.assertEqual(list(response.context['agendamentos']), [
                         self.agendamento1, self.agendamento2])

    def test_cliente_ve_apenas_seus_agendamentos(self):
        self.client.force_login(self.cliente1.user)
        response = self.client.get(reverse('agendamento-list'))
        self.assertEqual(list(response.context['agendamentos']), [
                         self.agendamento1])


class AgendamentoUpdateViewTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username='staff2', password='123456', is_staff=True)
        self.cliente = criar_cliente('cliente3', '14922220000')

        self.agendamento_proximo = Agendamento.objects.create(
            cliente=self.cliente, data_hora=timezone.now() + timedelta(hours=10)
        )
        self.agendamento_distante = Agendamento.objects.create(
            cliente=self.cliente, data_hora=timezone.now() + timedelta(days=10)
        )

    def test_cliente_nao_pode_editar_agendamento_proximo(self):
        self.client.force_login(self.cliente.user)
        url = reverse('agendamento-update', args=[self.agendamento_proximo.id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('agendamento-list'))

    def test_cliente_pode_editar_agendamento_distante(self):
        self.client.force_login(self.cliente.user)
        url = reverse('agendamento-update',
                      args=[self.agendamento_distante.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_staff_pode_editar_mesmo_com_agendamento_proximo(self):
        self.client.force_login(self.staff)
        url = reverse('agendamento-update', args=[self.agendamento_proximo.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class AlterarStatusAgendamentoTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username='staff3', password='123456', is_staff=True)
        self.cliente = criar_cliente('cliente4', '14933330000')
        self.agendamento = Agendamento.objects.create(
            cliente=self.cliente, data_hora=timezone.now() + timedelta(days=3)
        )

    def test_staff_pode_alterar_status(self):
        self.client.force_login(self.staff)
        url = reverse('agendamento-status', args=[self.agendamento.id])
        self.client.post(url, {'status': StatusAgendamento.CONFIRMADO})
        self.agendamento.refresh_from_db()
        self.assertEqual(self.agendamento.status, StatusAgendamento.CONFIRMADO)

    def test_cliente_nao_pode_alterar_status(self):
        self.client.force_login(self.cliente.user)
        url = reverse('agendamento-status', args=[self.agendamento.id])
        response = self.client.post(
            url, {'status': StatusAgendamento.CONFIRMADO})
        self.assertEqual(response.status_code, 403)

    def test_status_invalido_nao_altera_nada(self):
        self.client.force_login(self.staff)
        url = reverse('agendamento-status', args=[self.agendamento.id])
        self.client.post(url, {'status': 'NAO_EXISTE'})
        self.agendamento.refresh_from_db()
        self.assertEqual(self.agendamento.status, StatusAgendamento.PENDENTE)


class AgendamentoDeleteViewTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username='staff4', password='123456', is_staff=True)
        self.cliente = criar_cliente('cliente5', '14944440000')
        self.agendamento = Agendamento.objects.create(
            cliente=self.cliente, data_hora=timezone.now() + timedelta(days=3)
        )

    def test_staff_pode_excluir(self):
        self.client.force_login(self.staff)
        url = reverse('agendamento-delete', args=[self.agendamento.id])
        self.client.post(url)
        self.assertFalse(Agendamento.objects.filter(
            id=self.agendamento.id).exists())

    def test_cliente_nao_pode_excluir(self):
        self.client.force_login(self.cliente.user)
        url = reverse('agendamento-delete', args=[self.agendamento.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Agendamento.objects.filter(
            id=self.agendamento.id).exists())
