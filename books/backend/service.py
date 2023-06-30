from base.backend.servicebase import ServiceBase
from books.models import Author, Category, Books, BookIssued, BookFees


class AuthorService(ServiceBase):
    """
    Author services for CRUD
    """
    manager = Author.objects

class CategoryService(ServiceBase):
    """ Category model CRUD function"""
    manager =  Category.objects

class BookService(ServiceBase):
    """ books model CRUD services"""
    manager = Books.objects

class BookIssuedService(ServiceBase):
    """ Book issued our CRUD service"""
    manager = BookIssued.objects

class BookFeesService(ServiceBase):
    """ Book Fees our CRUD service"""
    manager = BookFees.objects


