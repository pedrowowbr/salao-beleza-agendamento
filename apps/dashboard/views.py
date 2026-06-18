from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.utils import timezone
from django.views.generic import TemplateView

from apps.clientes.models import Cliente
from apps.servicos.models import Servico
from apps.agendamentos.models import (
    Agendamento,
    AgendamentoServico,
    StatusAgendamento
)


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class DashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        hoje = timezone.now()

        inicio_semana = (
            hoje.date()
            - timedelta(days=hoje.weekday())
        )

        fim_semana = (
            inicio_semana
            + timedelta(days=6)
        )

        context['total_clientes'] = Cliente.objects.count()
        context['total_servicos'] = Servico.objects.count()
        context['total_agendamentos'] = Agendamento.objects.count()

        context['agendamentos_semana'] = (
            Agendamento.objects.filter(
                data_hora__date__range=(
                    inicio_semana,
                    fim_semana
                )
            ).count()
        )

        context['agendamentos_concluidos'] = (
            Agendamento.objects.filter(
                status=StatusAgendamento.CONCLUIDO
            ).count()
        )

        context['agendamentos_confirmados'] = (
            Agendamento.objects.filter(
                status=StatusAgendamento.CONFIRMADO
            ).count()
        )

        servico_mais_solicitado = (
            AgendamentoServico.objects
            .values('servico__nome')
            .annotate(total=Count('id'))
            .order_by('-total')
            .first()
        )

        context['servico_mais_solicitado'] = servico_mais_solicitado

        return context
