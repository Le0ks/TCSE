from http import HTTPStatus

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def custom_404(request: HttpRequest, exception: Exception) -> HttpResponse:
    return render(
        request,
        template_name="errors/404.html",
        status=HTTPStatus.NOT_FOUND,
    )


def custom_500(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        template_name="errors/500.html",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
