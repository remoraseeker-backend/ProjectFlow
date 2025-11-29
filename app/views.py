from collections.abc import Callable
from typing import Any
from typing import Optional

from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views import View


class AppBaseView(View):
    template_name = ''
    extra_context = None

    @classmethod
    def as_view(cls, template_name: str, extra_context: Optional[dict[str, Any]] = None) -> Callable[..., HttpResponse]:
        return super().as_view(template_name=template_name, extra_context=extra_context)

    def get_context(self, context: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        new_context = dict() if self.extra_context is None else self.extra_context
        if context is None:
            return new_context
        new_context.update(context)
        return new_context


class HomeView(AppBaseView):
    def get(self, request: HttpRequest, *args, **kwargs):
        return render(
            request=request,
            template_name=self.template_name,
            context=self.get_context(),
        )
