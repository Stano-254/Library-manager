import json
import logging

from django.core import serializers
from django.forms.models import model_to_dict

from base.backend.service import StateService
from base.backend.transactionlogbase import TransactionLogBase
from base.backend.utils.utilities import validate_uuid4, validate_name
from books.backend.service import AuthorService, CategoryService, BookService, BookIssuedService, BookFeesService
from members.backend.service import MemberService

lgr = logging.getLogger(__name__)


class BooksAdministration(TransactionLogBase):
    """
    handle the administration functionality relating to Books including CRUD
    """

    # Author CRUD
    def create_author(self, request, **kwargs):
        """
        Endpoint to Add authors to the database
        :param request: Http request
        :param kwargs:key-value arguments / parameters for creation of author
        :return: dict with failed code or success
        """
        transaction = None
        try:
            transaction = self.log_transaction('CreateAuthor', request=request, user=request.user)
            if not transaction:
                return {'code': '900.500.500', 'message': 'Error with Author transaction'}
            first_name = kwargs.pop("first_name")
            last_name = kwargs.pop("last_name")
            salutation = kwargs.get('salutation')
            description = kwargs.get('description', None)
            author = AuthorService().create(
                first_name=first_name, last_name=last_name, salutation=salutation, description=description)
            if not author:
                self.mark_transaction_failed(transaction, message='Author not created', response_code='300.001.001')
                return {'code': '300.001.001', 'message': 'Author not created'}
            self.complete_transaction(transaction, message='Author created', response_code='100.000.000')
            resp = json.loads(serializers.serialize('json', [author, ]))[0].get('pk')
            return {'code': '100.000.000', 'message': 'Success', 'data': resp}
        except Exception as e:
            self.mark_transaction_failed(
                transaction, response=str(e), message='Error occurred in add Author', response_code='999.999.999')
            return {'code': '999.999.999', 'message': 'Error occurred during author creation'}

    def get_author(self, request, author_id):
        """
        Get author from database
        :param request: HttpRequest
        :param author_id: The unique identifier of an author
        :return: dict with Author obj or error code
        """
        try:
            auth = model_to_dict(AuthorService().get(pk=author_id))
            return {'code': '100.000.000', 'data': auth}
        except Exception as e:
            print(e)
            return {'code': '999.999.999', 'message': 'Unable to get author'}

    def get_authors(self, request, **kwargs):
        """
        Get authors from database
        :param request:
        :param kwargs:
        :return:list of all authors
        """
        try:
            authors = list(AuthorService().filter().values())
            return {'code': '100.000.000', 'data': authors}
        except Exception as e:
            lgr.exception(f"Error during fetch of authors {e}")
            return {'code': '999.999.999', 'message': 'Error retrieving authos'}

    def update_author(self, request, **kwargs):
        """
        update author from database
        :param request:
        :param kwargs:
        :return:
        """
        transaction = None
        try:
            transaction = self.log_transaction('UpdateAuthor', request=request, user=request.user)
            if not transaction:
                return {'code': '900.500.500', 'message': 'Update author transaction failed'}
            author_id = kwargs.pop('author_id')
            if not validate_uuid4(str(author_id)):
                self.mark_transaction_failed(
                    transaction, message="Invalid author identifier", response_code="300.001.004")
                return {'code': '300.001.004', 'message': 'Invalid author identifier'}
            author = AuthorService().get(id=author_id)
            if not author:
                self.mark_transaction_failed(transaction, message="Author not found", reponse_code='300.001.404')
                return {'code': '300.001.404', 'message': 'Author not found'}
            update_author = AuthorService().update(author.id, **kwargs)
            if not update_author:
                self.mark_transaction_failed(transaction, message='Author not update', response_code='300.001.002')
                return {'code': '300.001.002', 'message': 'Author update failed'}
            resp = model_to_dict(update_author)
            resp['state'] = StateService().get(id=resp.pop('state')).name
            self.complete_transaction(transaction, response_code='100.000.000', message='Success')
            return {'code': '100.000.000', 'message': 'Success', 'data': resp}
        except Exception as e:
            lgr.exception(f"Error Failed to update author {e}")
            return {'code': '999.999.999', 'message': 'Error updating author'}

    def delete_author(self, request, author_id):
        """
        update author from database
        :param request:Http Request
        :param author_id: the unique identifier of the author
        :return: status code
        """
        transaction = None
        try:
            transaction = self.log_transaction('DeleteAuthor', request=request, user=request.user)
            if not transaction:
                return {'code': '900.500.500', 'message': 'Delete Author transaction failed'}
            author = AuthorService().get(id=author_id)
            if not author:
                self.mark_transaction_failed(transaction, message='Author not found', repsonse_code='300.001.004')
                return {'code': '300.001.004', 'message': 'Author not found'}
            update_author = AuthorService().update(author.id, state=StateService().get(name="Deleted"))
            if not update_author:
                self.mark_transaction_failed(
                    transaction, message='Failed to mark author as deleted', response_code='300.001.003')
                return {'code': '300.001.003', 'message': 'Author not deleted'}
            self.complete_transaction(transaction, message='Success', response_code='100.000.000')
            return {'code': '100.000.000', 'message': 'Success'}
        except Exception as e:
            self.mark_transaction_failed(
                transaction, message='Error occured during delete author', response=str(e), response_code='999.999.999')
            return {'code': '999.999.999', 'message': 'Error occurred durinf deletion of author'}

    # Category CRUD
    def create_category(self, request, **kwargs):
        """
        Add category to the database
        :param request: HttpRequest
        :param kwargs:key-value arguments
        :return: dict with response code for success or failure
        """
        transaction = None
        try:
            transaction = self.log_transaction("CreateCategory", request=request, user=request.user)
            if not transaction:
                return {'code': '900.500.500', 'message': 'Create category transaction failed'}
            name = kwargs.pop('name')
            if not validate_name(name):
                self.mark_transaction_failed(transaction, message="Invalid name provide", response_code='500.400.001')
                return {'code': '500.400.001', 'message': 'Invalid name provide'}
            category = CategoryService().create(name=name, **kwargs)
            if not category:
                self.mark_transaction_failed(
                    transaction, message='Failed to created category', response_code='300.002.002')
                return {'code': '300.002.002', 'message': 'Failed to created category'}
            self.complete_transaction(transaction, message='success')
            return {'code': '100.000.000', 'message': 'Success', 'data': model_to_dict(category)}
        except Exception as e:
            lgr.exception(f"Error occurred during category creation: {e}")
            self.mark_transaction_failed(
                transaction, message='Error Occurred during create category',
                response=str(e), response_code='999.999.999')
            return {'code': '999.999.999', 'message': 'Error Occurred during create category'}

    def get_category(self, request, category_id):
        """
        Get author from database
        :param request: HttpRequest
        :param category_id: the unique identifier for category
        :return: return dict of the data | None
        """
        try:
            if not validate_uuid4(category_id):
                return {'code': '500.400.004', 'message': 'Invalid category identifier'}
            category = CategoryService().get(id=category_id)
            if not category:
                return {'code': '300.002.003', 'message': 'Category not found'}
            return {'code': '100.000.000', 'data': model_to_dict(category)}
        except Exception as e:
            lgr.exception(f"Failed to fetch category with Error : {e}")
            return {'code': '999.999.999', 'message': 'An error occurred during get category'}

    def get_categories(self, request, **kwargs):
        """
        Get categories from database
        :param request:HttpRequest
        :param kwargs:
        :return: return queryset | []
        """
        try:
            categories = CategoryService().filter().values()
            if not categories:
                return {'code': '300.002.003', 'message': 'No categories found'}
            return {'code': '100.000.000', 'data': list(categories)}
        except Exception as e:
            lgr.exception(f"Failed to fetch categories with the following error : {e}")
            return {'code': '999.999.999', 'message': 'Unable to retrieve records'}

    def update_category(self, request, **kwargs):
        """
        update category from database
        :param request:HttpRequest
        :param kwargs: key-value parameters for updating category
        :return:return updated data | failure code
        """
        transaction = None
        try:
            transaction = self.log_transaction('UpdateCategory', request=request, user=request.user)
            if not transaction:
                return {'code': '900.500.500', 'message': 'Updating category transaction failed'}
            category_id = kwargs.pop('category_id')
            if not validate_uuid4(category_id):
                self.mark_transaction_failed(
                    transaction, message='Invalid category identifier', response_code='500.400.004')
                return {'code': '500.400.004', 'message': 'Invalid category identifier'}
            category = CategoryService().get(id=category_id)
            if not category:
                self.mark_transaction_failed(transaction, message='Category not found', response_code='300.002.002')
                return {'code': '300.002.002', 'message': 'Category not found'}
            update_category = CategoryService().update(id=category.id, **kwargs)
            if not update_category:
                self.mark_transaction_failed(
                    transaction, message='Failed to update category', response_code='300.002.003')
                return {'code': '300.002.003', 'message': 'Failed to update category'}
            self.complete_transaction(transaction, message='Success', response_code='100.000.00')
            return {'code': '100.000.000', 'message': 'Success', 'data': model_to_dict(update_category)}
        except Exception as e:
            lgr.exception(f"Error during update category : {e}")
            self.mark_transaction_failed(transaction, message="Error during update category", response=str(e))

    def delete_category(self, request, category_id):
        """
        Delete Category from database
        :param request:HttpRequest
        :param category_id:
        :return: Success code | failure code
        """
        transaction = None
        try:
            transaction = self.log_transaction('DeleteCategory', request=request, user=request.user)
            if not transaction:
                return {'code': '900.500.500', 'message': 'Delete category transaction failed'}
            if not validate_uuid4(category_id):
                self.mark_transaction_failed(
                    transaction, message="Invalid category identifier", response_code='500.400.004')
                return {'code': '500.400.004', 'message': 'Invalid category identifier'}
            category = CategoryService().get(id=category_id)
            if not category:
                self.mark_transaction_failed(transaction, message='Category not found', response_code='300.002.002')
                return {'code': '300.002.002', 'message': 'Category not found'}
            update_category = CategoryService().update(category.id, state=StateService().get(name='Deleted'))
            if not update_category:
                self.mark_transaction_failed(
                    transaction, message='Failed to delete category', response_code='300.002.003')
                return {'code': '300.002.003', 'message': 'Error occurred during delete category'}
        except Exception as e:
            lgr.exception(f"Error during delete category: {e}")
            self.mark_transaction_failed(transaction, message="Error Deleting Category", response=str(e))
            return {'code': '999.999.999', 'message': 'Error occurred during deletion of category'}

    # Book CRUD
    def create_book(self, request, **kwargs):
        """
          Handles adding of books in the library system
          :param request: the original request
          :param kwargs: keyword arguments for creation of book.
          :return: dict response with code 
          """
        transaction = None
        try:
            transaction = self.log_transaction(transaction_type="CreateBook", request=request, user=request.user)
            if not transaction:
                return {'code': '900.500.500', 'message': 'Transaction Failed'}
            author_id = kwargs.pop('author')
            category_id = kwargs.pop('category')
            author = AuthorService().get(id=author_id) if validate_uuid4(author_id) else AuthorService().filter(
                name=author_id).first()
            if not author:
                self.mark_transaction_failed(transaction, message="Author not found", response_code="300.001.001")
                return {'code': '300.001.001', 'message': 'Author not found'}

            kwargs['author'] = author
            category = CategoryService().get(id=category_id) if validate_uuid4(
                category_id) else CategoryService().filter(name=category_id).first()
            if not category:
                self.mark_transaction_failed(transaction, message="Category not found", response_code="300.002.001")
                return {'code': '300.002.001', 'message': 'Category not found'}
            kwargs['category'] = category
            book = BookService().create(**kwargs)
            if not book:
                self.mark_transaction_failed(
                    transaction, message="Unable to create book record", response_code="300.003.003")
                return {'code': '300.003.003', 'message': 'Unable to create book record'}
            self.complete_transaction(transaction, response_code='100.000.000' + 'Success', )
            return {'code': '100.000.000', 'message': 'success'}
        except Exception as e:
            self.mark_transaction_failed(transaction, response=str(e), response_code="999.999.999")
            return {'code': '999.999.999', 'message': 'Error Occurred during book creation'}

    def get_book(self, request, book_id):
        """
        handle fetching of one book
        :param request: original request as received
        :param book_id: the unique identifier of the book
        :return: HttpResponse with book data
        """
        try:
            if not validate_uuid4(book_id):
                return {'code': '500.400.004', 'message': 'Invalid book identifier'}
            book = BookService().get(id=book_id)
            if not book:
                return {'code': '300.003.002', 'message': 'No book record found'}
            return {'code': '100.000.000', 'data': model_to_dict(book)}
        except Exception as e:
            lgr.exception(f"Error during fetch book : {e}")
            return {'code': '999.999.999', 'message': 'Error during fetch book'}

    def get_books(self, request, **kwargs):
        """
        Handles fetching of multiple books, either with added conditions
        (like active books or archived books etc.) or without conditions
        :param request: original request received 
        :param kwargs: The parameters used to filter based on conditions if any.
        :return: dict response of a list of all books based on conditions provided
        """
        try:
            books = BookService().filter().values()
            if not books:
                return {'code': '300.003.002', 'message': 'No book records found'}
            return {'code': '100.000.000', 'data': list(books)}
        except Exception as e:
            lgr.exception(f"Error occurred during fetch books : {e}")
            return {'code': '999.999.999', 'message': 'Error occurred during fetch books'}

    def update_book(self, request, **kwargs):
        """
        Handles updating of books personal information or 
        any other information related to books
        :param request: Original Django HTTP request
        :type request: WSGIRequest
        :param book_id: 
        :param kwargs: dict of other parameters 
        :return: dict response
        """
        transaction = None
        try:
            transaction = self.log_transaction('UpdateBook', request=request, user=request.user)
            if not transaction:
                return {'code': '900.500.500', 'message': 'Update book transaction failed'}
            book_id = kwargs.pop('book_id')
            if not validate_uuid4(book_id):
                self.mark_transaction_failed(
                    transaction, message='Invalid book identifier', response_code='300.003.004')
                return {'code': '300.003.004', 'message': 'Invalid book identifier'}
            book = BookService().get(id=book_id)
            if not book:
                self.mark_transaction_failed(transaction, message="Book not found", response_code='300.003.002')
                return {'code': '300.003.002', 'message': 'Book not found'}
            update_book = BookService().update(book.id, **kwargs)
            if not update_book:
                self.mark_transaction_failed(
                    transaction, message='Failed to update the book record', response_code='300.003.003')
                return {'code': '300.003.003', 'message': 'Failed to update the book record'}

            self.complete_transaction(transaction, message='100.000.000', response_code='100.000.000')
            return {'code': '100.00.000', 'message': 'Success', 'data': model_to_dict(update_book)}
        except Exception as e:
            lgr.exception(f"Error occurred in update book : {e}")
            self.mark_transaction_failed(
                transaction, message="Error Occurred during update book record",
                response=str(e), response_code='999.999.999')
            return {'code': '999.999.999', 'message': 'Error occurred during update book'}

    def delete_book(self, request, book_id):
        """
        Handles deletion of a book from the system hypothetically
        though the book is never deleted just updated to state deleted
        :param request: Original Django HTTP request
        :param book_id: the unique book identifier
        :return: dict response with code
        """
        transaction = None
        try:
            transaction = self.log_transaction("DeleteBook", request=request, user=request.user)
            if not transaction:
                return {'code': '900.500.500', 'message': 'Delete book transaction failed'}
            if not validate_uuid4(book_id):
                self.mark_transaction_failed(transaction, message="Invalid book identifier",
                                             response_code='300.003.004')
                return {'code': '300.003.004', 'message': 'Invalid book identifier'}
            book = BookService().get(id=book_id)
            if not book:
                self.mark_transaction_failed(transaction, message='Book not found', response_code='300.003.002')
                return {'code': '300.003.002', 'message': 'Book not found'}
            updated_book = BookService().update(book.id, state=StateService().get(name='Deleted'))
            if not updated_book:
                self.mark_transaction_failed(transaction, message='Failed to delete book', response_code='300.003.003')
                return {'code': '300.003.003', 'message': 'Failed to delete book'}
            self.complete_transaction(transaction, message='Success')
            return {'code': '100.000.000', 'message': 'Success'}
        except Exception as e:
            lgr.exception(f"Error during deletion of book : {e}")
            self.mark_transaction_failed(transaction, message='Failed to delete the book', response=str(e))
            return {'code': '999.999.999', 'message': 'Error Failed to delete book record'}

    def archive_book(self, request, book_id):
        """
        Handles archiving  of a book from the system, i.e. updated to state archived
        :param request: Original Django HTTP request
        :param book_id: the unique book identifier
        :return: dict response with code
        """
        transaction = None
        try:
            transaction = self.log_transaction('ArchiveBook', request=request, user=request.user)
            if not transaction:
                return {'code': '900.500.500', 'message': 'Archive book transaction failed'}
            if not validate_uuid4(book_id):
                self.mark_transaction_failed(transaction, message="Invalid book identifier",
                                             response_code='300.003.004')
                return {'code': '300.003.004', 'message': 'Invalid book identifier'}
            book = BookService().get(id=book_id)
            if not book:
                self.mark_transaction_failed(transaction, message='Book not found', response_code='300.003.002')
                return {'code': '300.003.002', 'message': 'Book not found'}
            updated_book = BookService().update(book.id, state=StateService().get(name='Archived'))
            if not updated_book:
                self.mark_transaction_failed(transaction, message='Failed to archive book', response_code='300.003.003')
                return {'code': '300.003.003', 'message': 'Failed to archive book'}
            self.complete_transaction(transaction, message='Success')
            return {'code': '100.000.000', 'message': 'Success'}
        except Exception as e:
            lgr.exception(f"Error during archiving of book : {e}")
            self.mark_transaction_failed(transaction, message='Failed to archive the book', response=str(e))
            return {'code': '999.999.999', 'message': 'Error Failed to archive book record'}

    def borrow_book(self, request, book_id, member_id, **kwargs):
        """
        Handles borrowing of a book from the system, i.e. then reduce the number of available books
        :param member_id: the unique member identifier
        :param request: Original Django HTTP request
        :param book_id: the unique book identifier
        :return: dict response with code
        """
        transaction = None
        try:
            transaction = self.log_transaction('BorrowBook', request=request, user=request.user)
            if not transaction:
                return {'code': '900.500.500', 'message': 'Borrow book transaction failed'}
            borrow_duration = kwargs.get('borrow_duration', 7)
            if not validate_uuid4(book_id):
                self.mark_transaction_failed(
                    transaction, message="Invalid book identifier", response_code='300.003.004')
                return {'code': '300.003.004', 'message': 'Invalid book identifier'}
            book = BookService().get(id=book_id)
            if not book:
                self.mark_transaction_failed(transaction, message='Book not found', response_code='300.003.002')
                return {'code': '300.003.002', 'message': 'Book not found'}
            if not validate_uuid4(member_id):
                self.mark_transaction_failed(
                    transaction, message="Invalid member identifier", response_code='300.003.004')
                return {'code': '300.003.004', 'message': 'Invalid member identifier'}
            member = MemberService().get(id=member_id)
            if not member:
                self.mark_transaction_failed(transaction, message='Member not found', response_code='200.001.002')
                return {'code': '200.001.002', 'message': 'Member not found'}
            # check if the number of remaining books is greater than the number of reserve books
            if book.no_of_books <= book.no_of_reserve_books:
                self.mark_transaction_failed(
                    transaction, message="Book not available for borrowing", response_code='300.003.005')
                return {'code': '300.003.005', 'message': 'Book not available for borrowing'}
            # check if the member is eligible to borrow a book
            total_pending_fee = 0
            if BookIssuedService().filter(member=member):
                total_pending_fee = BookIssuedService().filter(member=member).first().total_pending_fee
            book_fee = BookFeesService().filter().first()
            if not book_fee:
                self.mark_transaction_failed(transaction, message='Failed to get book fees', response_code='300.004.002')
                return {'code': '300.004.002', 'message': 'Failed to get book fees'}
            if total_pending_fee >= book_fee.max_borrow_fee_limit:
                self.mark_transaction_failed(
                    transaction, message='Member not eligible to borrow book due to uncleared fees',
                    response_code='200.001.007')
                return {'code': '200.001.007', 'message': 'Member not eligible to borrow book due to uncleared fees'}
            updated_book = BookService().update(book.id, no_of_books=book.no_of_books - 1)
            if not updated_book:
                self.mark_transaction_failed(transaction, message='Failed to borrow book', response_code='300.003.006')
                return {'code': '300.003.006', 'message': 'Failed to borrow book'}
            book_issued = BookIssuedService().create(
                book=book, member=member, borrow_duration=borrow_duration,
                total_pending_fee=total_pending_fee + book_fee.borrow_fee, return_fee=book_fee.borrow_fee)
            if not book_issued:
                self.mark_transaction_failed(transaction, message='Failed to issued book ', response_code='300.003.003')
                return {'code': '300.003.003', 'message': 'Failed to issued book'}
            self.complete_transaction(transaction, message='Success')
            return {'code': '100.000.000', 'message': 'Success'}
        except Exception as e:
            lgr.exception(f"Error during borrowing of book : {e}")
            self.mark_transaction_failed(transaction, message='Failed to borrower the book', response=str(e))
            return {'code': '999.999.999', 'message': 'Error Failed to borrower book record'}

    def return_book(self, request, book_id, member_id):
        """
        Handles archiving  of a book from the system, i.e. updated to state archived
        :param member_id: the unique member identifier
        :param request: Original Django HTTP request
        :param book_id: the unique book identifier
        :return: dict response with code
        """
        transaction = None
        try:
            transaction = self.log_transaction('ReturnBook', request=request, user=request.user)
            if not transaction:
                return {'code': '900.500.500', 'message': 'Return book transaction failed'}
            if not validate_uuid4(book_id):
                self.mark_transaction_failed(
                    transaction, message="Invalid book identifier", response_code='300.003.004')
                return {'code': '300.003.004', 'message': 'Invalid book identifier'}
            book = BookService().get(id=book_id)
            if not book:
                self.mark_transaction_failed(transaction, message='Book not found', response_code='300.003.002')
                return {'code': '300.003.002', 'message': 'Book not found'}
            if not validate_uuid4(member_id):
                self.mark_transaction_failed(
                    transaction, message="Invalid member identifier", response_code='300.003.004')
                return {'code': '300.003.004', 'message': 'Invalid member identifier'}
            member = MemberService().get(id=member_id)
            if not member:
                self.mark_transaction_failed(transaction, message='Member not found', response_code='200.001.002')
                return {'code': '200.001.002', 'message': 'Member not found'}
            updated_book = BookService().update(book.id, no_of_books=book.no_of_books + 1)
            if not updated_book:
                self.mark_transaction_failed(transaction, message='Failed to archive book', response_code='300.003.003')
                return {'code': '300.003.003', 'message': 'Failed to archive book'}
            book_issued = BookIssuedService().filter(book=book, member=member, returned=False).first()
            if not book_issued:
                self.mark_transaction_failed(transaction, message='Failed to issued book ', response_code='300.003.003')
                return {'code': '300.003.003', 'message': 'Failed to issued book'}
            update_issued = BookIssuedService().update(
                book_issued.id, total_pending_fee=book_issued.total_pending_fee - book_issued.return_fee,
                fee_paid=True, returned=True)
            if not update_issued:
                self.mark_transaction_failed(transaction, message='Failed to return book ', response_code='300.003.008')
                return {'code': '300.003.008', 'message': 'Failed to return book'}
            self.complete_transaction(transaction, message='Success')
            return {'code': '100.000.000', 'message': 'Success'}
        except Exception as e:
            lgr.exception(f"Error during return book : {e}")
            self.mark_transaction_failed(transaction, message='Failed to return book', response=str(e))
            return {'code': '999.999.999', 'message': 'Error Failed to return book record'}
