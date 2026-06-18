from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import (
    redirect,
    get_object_or_404
)
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView
)

from .forms import AgendamentoForm
from .models import (
    Agendamento,
    AgendamentoServico,
    StatusAgendamento
)
from .services.agendamento_service import (
    AgendamentoService
)


def agendamentos_do_usuario(user):
    if user.is_staff:
        return Agendamento.objects.all()

    if hasattr(user, 'cliente'):
        return Agendamento.objects.filter(cliente=user.cliente)

    return Agendamento.objects.none()


class AgendamentoListView(LoginRequiredMixin, ListView):
    model = Agendamento
    template_name = 'agendamentos/list.html'
    context_object_name = 'agendamentos'

    def get_queryset(self):
        queryset = agendamentos_do_usuario(self.request.user)

        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if data_inicio:
            queryset = queryset.filter(
                data_hora__date__gte=data_inicio
            )

        if data_fim:
            queryset = queryset.filter(
                data_hora__date__lte=data_fim
            )

        return queryset


class AgendamentoCreateView(LoginRequiredMixin, CreateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'agendamentos/form.html'
    success_url = reverse_lazy('agendamento-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if not self.request.user.is_staff:
            form.fields.pop('cliente', None)

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agendamento_existente'] = getattr(
            self,
            'agendamento_existente',
            None
        )
        context['agendamento_existente_pode_editar'] = getattr(
            self,
            'agendamento_existente_pode_editar',
            False
        )
        context['agendamento_existente_url'] = getattr(
            self,
            'agendamento_existente_url',
            None
        )
        return context

    def form_valid(self, form):
        if self.request.user.is_staff:
            cliente = form.cleaned_data['cliente']
        else:
            if not hasattr(self.request.user, 'cliente'):
                raise PermissionDenied

            cliente = self.request.user.cliente

        data_hora = form.cleaned_data['data_hora']
        servicos = form.cleaned_data['servicos']

        agendamento_existente = AgendamentoService.buscar_agendamento_mesma_semana(
            cliente,
            data_hora
        )

        confirmar_mesmo_assim = self.request.POST.get(
            'confirmar_mesmo_assim'
        ) == '1'

        if agendamento_existente and not confirmar_mesmo_assim:
            self.agendamento_existente = agendamento_existente
            self.agendamento_existente_pode_editar = AgendamentoService.pode_alterar(
                agendamento_existente
            )
            self.agendamento_existente_url = reverse(
                'agendamento-update',
                args=[agendamento_existente.id]
            )

            return self.render_to_response(
                self.get_context_data(form=form)
            )

        form.instance.cliente = cliente
        response = super().form_valid(form)

        for servico in servicos:
            AgendamentoServico.objects.create(
                agendamento=self.object,
                servico=servico
            )

        return response


class AgendamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'agendamentos/form.html'
    success_url = reverse_lazy('agendamento-list')

    def get_queryset(self):
        return agendamentos_do_usuario(self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if not self.request.user.is_staff:
            form.fields.pop('cliente', None)

        return form

    def dispatch(self, request, *args, **kwargs):
        agendamento = self.get_object()

        if not request.user.is_staff and not AgendamentoService.pode_alterar(agendamento):
            return redirect('agendamento-list')

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def form_valid(self, form):
        if self.request.user.is_staff:
            cliente = form.cleaned_data['cliente']
        else:
            if not hasattr(self.request.user, 'cliente'):
                raise PermissionDenied

            cliente = self.request.user.cliente

        servicos = form.cleaned_data['servicos']

        form.instance.cliente = cliente
        response = super().form_valid(form)

        self.object.itens_servico.all().delete()

        for servico in servicos:
            AgendamentoServico.objects.create(
                agendamento=self.object,
                servico=servico
            )

        return response


class AgendamentoDetailView(LoginRequiredMixin, DetailView):
    model = Agendamento
    template_name = 'agendamentos/detail.html'
    context_object_name = 'agendamento'

    def get_queryset(self):
        return agendamentos_do_usuario(self.request.user)


@login_required
def alterar_status_agendamento(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method != 'POST':
        return redirect('agendamento-list')

    agendamento = get_object_or_404(Agendamento, pk=pk)
    novo_status = request.POST.get('status')

    status_validos = {
        StatusAgendamento.PENDENTE,
        StatusAgendamento.CONFIRMADO,
        StatusAgendamento.EM_ANDAMENTO,
        StatusAgendamento.CONCLUIDO,
        StatusAgendamento.CANCELADO,
    }

    if novo_status not in status_validos:
        messages.error(request, 'Status inválido.')
        return redirect('agendamento-list')

    agendamento.status = novo_status
    agendamento.save()

    messages.success(
        request,
        f'Status do agendamento atualizado para {agendamento.get_status_display()}.'
    )

    return redirect('agendamento-list')


@login_required
def confirmar_agendamento(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    agendamento = get_object_or_404(
        Agendamento,
        pk=pk
    )

    AgendamentoService.confirmar_agendamento(
        agendamento
    )

    return redirect(
        'agendamento-list'
    )


@login_required
def cancelar_agendamento(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    agendamento = get_object_or_404(
        Agendamento,
        pk=pk
    )

    AgendamentoService.cancelar_agendamento(
        agendamento
    )

    return redirect(
        'agendamento-list'
    )


@login_required
def agendamento_delete(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method != 'POST':
        return redirect('agendamento-list')

    agendamento = get_object_or_404(Agendamento, pk=pk)
    agendamento.delete()

    messages.success(request, 'Agendamento excluído com sucesso.')
    return redirect('agendamento-list')
