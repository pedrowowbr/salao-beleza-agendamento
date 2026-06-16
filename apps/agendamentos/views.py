from django.shortcuts import render
from .models import AgendamentoService, Agendamento
from django.contrib import messages

# Create your views here.


def alterar_agendamento(request, id_agendamento):
    agendamento = Agendamento.objects.get(id=id_agendamento)
    if not AgendamentoService.pode_alterar(agendamento):
        messages.error(request,
                       "Alterações somente por telefone. Entre em contato conosco para mais informações.")
