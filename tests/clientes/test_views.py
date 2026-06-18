from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.clientes.models import Cliente


class ClienteCreateViewTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username='staffc', password='123456', is_staff=True)
        self.cliente_user = User.objects.create_user(
            username='clientec', password='123456')

    def test_apenas_staff_acessa_criacao(self):
        self.client.force_login(self.cliente_user)
        response = self.client.get(reverse('cliente-create'))
        self.assertEqual(response.status_code, 403)

    def test_staff_cria_cliente_com_usuario_vinculado(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse('cliente-create'), {
            'nome': 'Nova Cliente', 'email': 'nova@example.com', 'telefone': '14966660000',
            'endereco': 'Rua F, 30', 'username': 'novacliente', 'password': 'senha123'
        })
        self.assertEqual(response.status_code, 302)

        cliente = Cliente.objects.get(telefone='14966660000')
        self.assertEqual(cliente.user.username, 'novacliente')
        self.assertTrue(cliente.user.check_password('senha123'))


class ClienteUpdateViewTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username='staffu', password='123456', is_staff=True)
        user = User.objects.create_user(
            username='antigo', password='senhaantiga')
        self.cliente = Cliente.objects.create(
            user=user, nome='Antigo Nome', email='antigo@example.com',
            telefone='14977770000', endereco='Rua G, 40'
        )

    def test_atualiza_username_sem_alterar_senha(self):
        self.client.force_login(self.staff)
        self.client.post(reverse('cliente-update', args=[self.cliente.pk]), {
            'nome': 'Antigo Nome', 'email': 'antigo@example.com', 'telefone': '14977770000',
            'endereco': 'Rua G, 40', 'username': 'novonome'
        })
        self.cliente.user.refresh_from_db()
        self.assertEqual(self.cliente.user.username, 'novonome')
        self.assertTrue(self.cliente.user.check_password('senhaantiga'))

    def test_atualiza_senha_quando_informada(self):
        self.client.force_login(self.staff)
        self.client.post(reverse('cliente-update', args=[self.cliente.pk]), {
            'nome': 'Antigo Nome', 'email': 'antigo@example.com', 'telefone': '14977770000',
            'endereco': 'Rua G, 40', 'username': 'antigo', 'password': 'novasenha'
        })
        self.cliente.user.refresh_from_db()
        self.assertTrue(self.cliente.user.check_password('novasenha'))


class ClienteDeleteViewTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username='staffd', password='123456', is_staff=True)
        user = User.objects.create_user(username='excluir', password='123456')
        self.cliente = Cliente.objects.create(
            user=user, nome='Vai Sair', email='sair@example.com',
            telefone='14988880000', endereco='Rua H, 50'
        )

    def test_staff_exclui_cliente_e_usuario(self):
        self.client.force_login(self.staff)
        self.client.post(reverse('cliente-delete', args=[self.cliente.pk]))
        self.assertFalse(Cliente.objects.filter(pk=self.cliente.pk).exists())
        self.assertFalse(User.objects.filter(username='excluir').exists())
