from django import forms
from .models import Servico


class ServicoForm(forms.ModelForm):

    class Meta:
        model = Servico
        fields = '__all__'

        widgets = {
            'nome': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'descricao': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),
            'preco': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'duracao_minutos': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
        }
