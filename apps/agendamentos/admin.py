from django.contrib import admin

# Register your models here.
from .models import (
    Agendamento,
    AgendamentoServico
)

admin.site.register(Agendamento)
admin.site.register(AgendamentoServico)
