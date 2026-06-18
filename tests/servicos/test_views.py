from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.servicos.models import Servico


class ServicoListViewTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username='staff_s1', password='123456', is_staff=True)
        self.comum = User.objects.create_user(
            username='comum_s1', password='123456')

    def test_redireciona_usuario_nao_logado(self):
        response = self.client.get(reverse('servico-list'))
        self.assertEqual(response.status_code, 302)

    def test_usuario_comum_nao_acessa_lista(self):
        self.client.force_login(self.comum)
        response = self.client.get(reverse('servico-list'))
        self.assertEqual(response.status_code, 403)

    def test_staff_acessa_lista(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse('servico-list'))
        self.assertEqual(response.status_code, 200)


class ServicoCreateViewTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username='staff_s2', password='123456', is_staff=True)
        self.comum = User.objects.create_user(
            username='comum_s2', password='123456')

    def test_usuario_comum_nao_pode_criar(self):
        self.client.force_login(self.comum)
        response = self.client.get(reverse('servico-create'))
        self.assertEqual(response.status_code, 403)

    def test_staff_cria_servico(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse('servico-create'), {
            'nome': 'Corte de Cabelo',
            'descricao': 'Corte simples',
            'preco': '50.00',
            'duracao_minutos': '30'
        })

        self.assertEqual(response.status_code, 302)
        servico = Servico.objects.get(nome='Corte de Cabelo')
        self.assertEqual(servico.preco, Decimal('50.00'))
        self.assertEqual(servico.duracao_minutos, 30)


class ServicoUpdateViewTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username='staff_s3', password='123456', is_staff=True)
        self.servico = Servico.objects.create(
            nome='Manicure', descricao='Manicure simples',
            preco=Decimal('25.00'), duracao_minutos=40
        )

    def test_staff_atualiza_servico(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse('servico-update', args=[self.servico.pk]), {
            'nome': 'Manicure Completa',
            'descricao': 'Manicure com decoração',
            'preco': '35.00',
            'duracao_minutos': '50'
        })

        self.assertEqual(response.status_code, 302)
        self.servico.refresh_from_db()
        self.assertEqual(self.servico.nome, 'Manicure Completa')
        self.assertEqual(self.servico.preco, Decimal('35.00'))


class ServicoDeleteViewTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username='staff_s4', password='123456', is_staff=True)
        self.comum = User.objects.create_user(
            username='comum_s4', password='123456')
        self.servico = Servico.objects.create(
            nome='Escova', descricao='Escova progressiva',
            preco=Decimal('80.00'), duracao_minutos=60
        )

    def test_staff_exclui_servico(self):
        self.client.force_login(self.staff)
        self.client.post(reverse('servico-delete', args=[self.servico.pk]))
        self.assertFalse(Servico.objects.filter(pk=self.servico.pk).exists())

    def test_usuario_comum_nao_pode_excluir(self):
        self.client.force_login(self.comum)
        response = self.client.post(
            reverse('servico-delete', args=[self.servico.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Servico.objects.filter(pk=self.servico.pk).exists())

    def test_get_nao_exclui(self):
        self.client.force_login(self.staff)
        self.client.get(reverse('servico-delete', args=[self.servico.pk]))
        self.assertTrue(Servico.objects.filter(pk=self.servico.pk).exists())
