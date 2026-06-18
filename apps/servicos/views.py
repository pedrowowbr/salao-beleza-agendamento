from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView
)

from .models import Servico
from .forms import ServicoForm


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ServicoListView(StaffRequiredMixin, ListView):
    model = Servico
    template_name = 'servicos/list.html'
    context_object_name = 'servicos'


class ServicoCreateView(StaffRequiredMixin, CreateView):
    model = Servico
    form_class = ServicoForm
    template_name = 'servicos/form.html'
    success_url = reverse_lazy('servico-list')


class ServicoUpdateView(StaffRequiredMixin, UpdateView):
    model = Servico
    form_class = ServicoForm
    template_name = 'servicos/form.html'
    success_url = reverse_lazy('servico-list')


@login_required
def servico_delete(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method != 'POST':
        return redirect('servico-list')

    servico = get_object_or_404(Servico, pk=pk)
    servico.delete()

    messages.success(request, 'Serviço excluído com sucesso.')
    return redirect('servico-list')
