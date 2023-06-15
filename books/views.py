import logging

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from base.backend.utils.utilities import get_request_data
from books.administration.books_administration import BooksAdministration

lgr = logging.getLogger(__name__)
# Create your views here.
@csrf_exempt
def index(request):
    return HttpResponse("books oks")

@csrf_exempt
def create_book(request):
    try:
        kwargs = get_request_data(request)
        return JsonResponse(BooksAdministration().create_book(request, **kwargs))
    except Exception as e:
        lgr.exception(f"Create book error {e}")
        return JsonResponse({'code':"500.000.100","message":"Failure during book creation"})

urlpatterns = [
    re_path(r'^get_book/$', index),
    re_path(r'^create_book/$', create_book),
]