from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import ClienteRegisterForm


class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('dashboard')
        return reverse_lazy('agendamento-list')


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('accounts:login')


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = ClienteRegisterForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
