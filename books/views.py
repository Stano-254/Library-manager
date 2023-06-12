from django.http import HttpResponse
from django.shortcuts import render
from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def index(request):
    return HttpResponse("books oks")

urlpatterns = [
    re_path(r'^get_book/$', index),
]