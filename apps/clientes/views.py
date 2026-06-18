from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView
)
from .forms import ClienteForm
from .models import Cliente


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ClienteListView(StaffRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/list.html'
    context_object_name = 'clientes'


class ClienteCreateView(StaffRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('cliente-list')

    def form_valid(self, form):
        with transaction.atomic():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data.get('email', '')
            )
            form.instance.user = user
            return super().form_valid(form)


class ClienteUpdateView(StaffRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('cliente-list')

    def form_valid(self, form):
        with transaction.atomic():
            user = self.object.user
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data.get('email', user.email)

            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data['password'])

            user.save()
            return super().form_valid(form)


@login_required
def cliente_delete(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method != 'POST':
        return redirect('cliente-list')

    cliente = get_object_or_404(Cliente, pk=pk)
    usuario = cliente.user
    usuario.delete()

    messages.success(request, 'Cliente excluído com sucesso.')
    return redirect('cliente-list')
