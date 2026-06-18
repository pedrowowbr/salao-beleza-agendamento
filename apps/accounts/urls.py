from django.urls import path

from .views import LoginView, LogoutView, RegisterView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registrar/', RegisterView.as_view(), name='register'),
]
