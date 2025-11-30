from django.conf import settings
from django.contrib.auth import login
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from authentication.forms import RegisterForm
from authentication.models import User


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'authentication/register.html'
    extra_context = {'page_title': 'Register'}

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = form.save()
        login(request=self.request, user=user)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return getattr(settings, 'REGISTER_REDIRECT_URL', reverse_lazy(viewname='app_home'))
