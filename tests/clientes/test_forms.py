from django.contrib.auth.models import User
from django.test import TestCase

from apps.clientes.forms import ClienteForm
from apps.clientes.models import Cliente


class ClienteFormCreateTests(TestCase):
    def test_form_valido_cria_usuario_e_cliente(self):
        form = ClienteForm(data={
            'nome': 'Ana', 'email': 'ana@example.com', 'telefone': '14955550000',
            'endereco': 'Rua C, 789', 'username': 'ana123', 'password': 'senha123'
        })
        self.assertTrue(form.is_valid())

    def test_senha_obrigatoria_na_criacao(self):
        form = ClienteForm(data={
            'nome': 'Ana', 'email': 'ana@example.com', 'telefone': '14955550001',
            'endereco': 'Rua C, 789', 'username': 'ana456'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_username_duplicado_invalida_form(self):
        User.objects.create_user(username='existente', password='123456')
        form = ClienteForm(data={
            'nome': 'Bia', 'email': 'bia@example.com', 'telefone': '14955550002',
            'endereco': 'Rua D, 10', 'username': 'existente', 'password': 'senha123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class ClienteFormUpdateTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='carlos', password='123456')
        self.cliente = Cliente.objects.create(
            user=user, nome='Carlos', email='carlos@example.com',
            telefone='14955550003', endereco='Rua E, 20'
        )

    def test_senha_opcional_na_edicao(self):
        form = ClienteForm(
            data={
                'nome': 'Carlos Silva', 'email': 'carlos@example.com',
                'telefone': '14955550003', 'endereco': 'Rua E, 20', 'username': 'carlos'
            },
            instance=self.cliente
        )
        self.assertTrue(form.is_valid())
