from django.http import HttpResponse
from django.shortcuts import render
from django.urls import re_path


# Create your views here.
def index():

    return HttpResponse("members ok")


urlpatterns = [
    re_path(r'^get_member/$', index),
    ]