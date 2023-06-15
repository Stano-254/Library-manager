import logging
from django.http import HttpResponse, JsonResponse
from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from base.backend.utils.utilities import get_request_data
from books.administration.books_administration import BooksAdministration

lgr = logging.getLogger(__name__)

@csrf_exempt
def create_author(request):
    try:
        kwargs = get_request_data(request)
        return JsonResponse(BooksAdministration().create_author(request, **kwargs))
    except Exception as e:
        lgr.exception(f"Create author error {e}")
        return JsonResponse({'code': "500.000.100", "message": "Failure during author creation"})


@csrf_exempt
def get_author(request):
    try:
        author_id = get_request_data(request).pop('author')
        return JsonResponse(BooksAdministration().get_author(request, author_id=author_id))
    except Exception as e:
        lgr.exception(f"Get author error {e}")
        return JsonResponse({'code': "500.000.100", "message": "Failure during fetch author"})


@csrf_exempt
def get_authors(request):
    try:
        kwargs = get_request_data(request)
        return JsonResponse(BooksAdministration().get_authors(request, **kwargs))
    except Exception as e:
        lgr.exception(f"Get authors error {e}")
        return JsonResponse({'code': "500.000.100", "message": "Failure during fetch authors"})


@csrf_exempt
def update_author(request):
    try:
        kwargs = get_request_data(request)
        return JsonResponse(BooksAdministration().get_authors(request, **kwargs))
    except Exception as e:
        lgr.exception(f"update author error {e}")
        return JsonResponse({'code': "500.000.100", "message": "Failure during update author"})


@csrf_exempt
def delete_author(request):
    try:
        author_id = get_request_data(request).pop('author')
        return JsonResponse(BooksAdministration().delete_author(request, author_id=author_id))
    except Exception as e:
        lgr.exception(f"Delete author error {e}")
        return JsonResponse({'code': "500.000.100", "message": "Failure during deletion of author"})


@csrf_exempt
def create_category(request):
    try:
        kwargs = get_request_data(request)
        return JsonResponse(BooksAdministration().create_category(request, **kwargs))
    except Exception as e:
        lgr.exception(f"Create category error {e}")
        return JsonResponse({'code': "500.000.100", "message": "Failure during category creation"})


@csrf_exempt
def get_category(request):
    try:
        category_id = get_request_data(request).pop('category')
        return JsonResponse(BooksAdministration().get_category(request, category_id))
    except Exception as e:
        lgr.exception(f"Get category error {e}")
        return JsonResponse({'code': "500.000.100", "message": "Failure during get category"})

@csrf_exempt
def get_categories(request):
    try:
        kwargs = get_request_data(request)
        return JsonResponse(BooksAdministration().get_categories(request, **kwargs))
    except Exception as e:
        lgr.exception(f"Get categories error {e}")
        return JsonResponse({'code': "500.000.100", "message": "Failure during fetch categories"})

@csrf_exempt
def update_category(request):
    try:
        kwargs = get_request_data(request)
        return JsonResponse(BooksAdministration().update_category(request, **kwargs))
    except Exception as e:
        lgr.exception(f"Update category error {e}")
        return JsonResponse({'code': "500.000.100", "message": "Failure during updating category"})

@csrf_exempt
def delete_category(request):
    try:
        category_id = get_request_data(request).pop('category')
        return JsonResponse(BooksAdministration().delete_category(request, category_id))
    except Exception as e:
        lgr.exception(f"Delete category error {e}")
        return JsonResponse({'code': "500.000.100", "message": "Failure during category deletion"})


@csrf_exempt
def create_book(request):
    try:
        kwargs = get_request_data(request)
        return JsonResponse(BooksAdministration().create_book(request, **kwargs))
    except Exception as e:
        lgr.exception(f"Create book error {e}")
        return JsonResponse({'code': "500.000.100", "message": "Failure during book creation"})

@csrf_exempt
def get_book(request):
    try:
        book_id = get_request_data(request).pop('book')
        return JsonResponse(BooksAdministration().get_book(request, book_id))
    except Exception as e:
        lgr.exception(f"Get book error {e}")
        return JsonResponse({'code': "500.000.100", "message": "Failure during get book"})

@csrf_exempt
def get_books(request):
    try:
        kwargs = get_request_data(request)
        return JsonResponse(BooksAdministration().get_books(request, **kwargs))
    except Exception as e:
        lgr.exception(f"Get books error {e}")
        return JsonResponse({'code': "500.000.100", "message": "Failure during fetch books"})

@csrf_exempt
def update_book(request):
    try:
        kwargs = get_request_data(request)
        return JsonResponse(BooksAdministration().update_book(request, **kwargs))
    except Exception as e:
        lgr.exception(f"Update book error {e}")
        return JsonResponse({'code': "500.000.100", "message": "Failure during update book"})

@csrf_exempt
def delete_book(request):
    try:
        book_id = get_request_data(request).pop('book')
        return JsonResponse(BooksAdministration().delete_book(request, book_id))
    except Exception as e:
        lgr.exception(f"Delete book error {e}")
        return JsonResponse({'code': "500.000.100", "message": "Failure during book deletion"})


urlpatterns = [
    # author
    re_path(r'^create_author',create_author),
    re_path(r'^get_author',get_author),
    re_path(r'^get_authors',get_authors),
    re_path(r'^update_author',get_author),
    re_path(r'^delete_author',delete_author),
    # category
    re_path(r'^create_category', create_category),
    re_path(r'^get_category', get_category),
    re_path(r'^get_categories', get_categories),
    re_path(r'^update_category', update_category),
    re_path(r'^delete_catregory', delete_category),
    # books
    re_path(r'^create_book/$', create_book),
    re_path(r'^create_book/$', get_book),
    re_path(r'^create_book/$', get_books),
    re_path(r'^create_book/$', update_book),
    re_path(r'^create_book/$', delete_book),
]
