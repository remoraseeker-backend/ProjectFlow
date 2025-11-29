from django.conf import settings
from django.contrib.auth import login
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.views import AppBaseView
from authentication.forms import RegisterForm
from authentication.models import User


class RegisterView(AppBaseView):
    def get(self, request: HttpRequest, *args, **kwargs):
        return render(
            request=request,
            template_name=self.template_name,
            context=self.get_context({'form': RegisterForm}),
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        form = RegisterForm(data=request.POST)
        if not form.is_valid():
            return HttpResponseRedirect(redirect_to=reverse(viewname='register'))

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = User.objects.filter(username=username).first()
        if user is None:
            user = User.objects.create_user(username=username, password=password)
            login(request=request, user=user)
            return HttpResponseRedirect(redirect_to=self.get_redirect_url())

        form.add_error(field=None, error='Incorrect username or password')
        return render(
            request=request,
            template_name=self.template_name,
            context=self.get_context({'form': form}),
        )

    def get_redirect_url(self) -> str:
        url = getattr(settings, 'REGISTER_REDIRECT_URL', reverse(viewname='home'))
        return url
