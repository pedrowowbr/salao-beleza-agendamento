from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.clientes.models import Cliente


class ClienteRegisterForm(UserCreationForm):
    email = forms.EmailField()
    nome = forms.CharField(max_length=100)
    telefone = forms.CharField(max_length=20)
    endereco = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'nome',
            'telefone',
            'endereco',
            'password1',
            'password2',
        ]

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Já existe um usuário com esse login.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() or Cliente.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Já existe um cadastro com esse e-mail.')
        return email

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if Cliente.objects.filter(telefone=telefone).exists():
            raise forms.ValidationError(
                'Já existe um cadastro com esse telefone.')
        return telefone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['nome']

        if commit:
            user.save()
            Cliente.objects.create(
                user=user,
                nome=self.cleaned_data['nome'],
                email=self.cleaned_data['email'],
                telefone=self.cleaned_data['telefone'],
                endereco=self.cleaned_data['endereco'],
            )

        return user
