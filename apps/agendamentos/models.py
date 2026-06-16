from django.db import models

# Create your models here.


class StatusAgendamento(models.TextChoices):
    PENDENTE = "PENDENTE", "Pendente"
    CONFIRMADO = "CONFIRMADO", "Confirmado"
    EM_ANDAMENTO = "EM_ANDAMENTO", "Em andamento"
    CONCLUIDO = "CONCLUIDO", "Concluído"
    CANCELADO = "CANCELADO", "Cancelado"


class Agendamento(models.Model):
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE)
    servico = models.ForeignKey('servicos.Servico', on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    observacao = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=StatusAgendamento.choices, default=StatusAgendamento.PENDENTE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cliente.nome} - {self.servico.nome} - {self.data_hora}"


class AgendamentoServico(models.Model):
    agendamento = models.ForeignKey(
        Agendamento, on_delete=models.CASCADE, related_name="servicos")
    servico = models.ForeignKey(
        'servicos.Servico', on_delete=models.CASCADE, related_name="agendamentos")

    def __str__(self):
        return f"{self.agendamento} - {self.servico.nome}"
