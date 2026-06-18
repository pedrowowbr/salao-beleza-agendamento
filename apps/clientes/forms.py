from django import forms
from django.contrib.auth.models import User
from .models import Cliente


class ClienteForm(forms.ModelForm):
    username = forms.CharField(
        label='Usuário',
        max_length=150
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = Cliente
        fields = [
            'nome',
            'email',
            'telefone',
            'endereco'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['username'].initial = self.instance.user.username
            self.fields['password'].help_text = 'Deixe em branco para manter a senha atual.'
        else:
            self.fields['password'].required = True

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username=username)

        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.user.pk)

        if qs.exists():
            raise forms.ValidationError('Esse nome de usuário já está em uso.')

        return username
