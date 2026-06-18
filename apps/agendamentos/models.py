from django.db import models


class StatusAgendamento(models.TextChoices):
    PENDENTE = "PENDENTE", "Pendente"
    CONFIRMADO = "CONFIRMADO", "Confirmado"
    EM_ANDAMENTO = "EM_ANDAMENTO", "Em andamento"
    CONCLUIDO = "CONCLUIDO", "Concluído"
    CANCELADO = "CANCELADO", "Cancelado"


class Agendamento(models.Model):

    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.CASCADE,
        related_name='agendamentos'
    )

    data_hora = models.DateTimeField()

    observacao = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=StatusAgendamento.choices,
        default=StatusAgendamento.PENDENTE
    )

    data_criacao = models.DateTimeField(
        auto_now_add=True
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['data_hora']
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return (
            f'{self.cliente.nome} - '
            f'{self.data_hora:%d/%m/%Y %H:%M}'
        )


class AgendamentoServico(models.Model):

    agendamento = models.ForeignKey(
        Agendamento,
        on_delete=models.CASCADE,
        related_name='itens_servico'
    )

    servico = models.ForeignKey(
        'servicos.Servico',
        on_delete=models.CASCADE,
        related_name='agendamentos'
    )

    class Meta:
        unique_together = (
            'agendamento',
            'servico'
        )

        verbose_name = 'Serviço do Agendamento'
        verbose_name_plural = 'Serviços do Agendamento'

    def __str__(self):
        return (
            f'{self.agendamento.cliente.nome} - '
            f'{self.servico.nome}'
        )
