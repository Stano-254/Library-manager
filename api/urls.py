from django.urls import re_path, include

from . import views

urlpatterns = [
    re_path(r'^books/', include('books.views'), name='books'),
    re_path(r'^members/', include('members.views'), name='members'),
    re_path(r'^auth/', include('base.backend.authentication'), name='login')
]
