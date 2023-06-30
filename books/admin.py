from django.contrib import admin

from books.models import Author, Category, Books, BookIssued, BookFees


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Author admin site
    """
    list_display = ('salutation', 'first_name','last_name', 'description', 'state', 'date_modified', 'date_created')
    search_fields = ('first_name','last_name')
    list_filter = ('state__name', 'date_created')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category admin site
    """
    list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
    search_fields = ('name',)
    list_filter = ('state__name', 'date_created')


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    """
    Books admin site
    """
    list_display = (
        'isbn', 'title', 'published_date', 'edition', 'book_image', 'author', 'category', 'status', 'date_modified',
        'date_created')
    search_fields = ('isbn', 'author', 'title')
    list_filter = ('status__name', 'date_created', 'author')


@admin.register(BookIssued)
class BookIssuedAdmin(admin.ModelAdmin):
    """
    Books admin site
    """
    list_display = (
        'book', 'member', 'issued_date', 'borrow_duration', 'return_date', 'return_fee', 'fee_paid', 'returned')
    search_fields = ('book__author', 'book__title', 'member__membership_no')
    list_filter = ('book__author', 'issued_date')
@admin.register(BookFees)
class BookFeesAdmin(admin.ModelAdmin):
    """
    Books admin site
    """
    list_display = ('borrow_fee', 'late_return_rate', 'max_borrow_fee_limit')
    search_fields = ('borrow_fee', 'late_return_rate', 'max_borrow_fee_limit')
