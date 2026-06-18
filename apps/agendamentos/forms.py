from django import forms
from apps.servicos.models import Servico
from .models import Agendamento


class ServicoMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, servico):
        preco_formatado = f'{servico.preco:.2f}'.replace('.', ',')
        return f'{servico.nome} - R$ {preco_formatado} ({servico.duracao_minutos} min)'


class AgendamentoForm(forms.ModelForm):
    servicos = ServicoMultipleChoiceField(
        queryset=Servico.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'form-check-input'}),
        required=True,
        label='Serviços'
    )

    class Meta:
        model = Agendamento
        fields = [
            'cliente',
            'data_hora',
            'observacao'
        ]
        widgets = {
            'data_hora': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['servicos'].initial = list(
                self.instance.itens_servico.values_list(
                    'servico_id',
                    flat=True
                )
            )
