from urllib.request import Request

from django.http import HttpResponse


def home(request: Request):
    return HttpResponse(content='This is the home page!')
