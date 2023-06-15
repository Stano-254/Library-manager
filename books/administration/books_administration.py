from base.backend.transactionlogbase import TransactionLogBase
from base.backend.utils.utilities import validate_uuid4
from books.backend.service import AuthorService, CategoryService, BookService


class BooksAdministration(TransactionLogBase):
    """
    handle the administration functionality relating to Books including CRUD
    """
    # Author CRUD
    def create_author(self, request, **kwargs):
        """
        Add authors to the database
        :param request:
        :param kwargs:
        :return:
        """
        pass

    def get_author(self, request, **kwargs):
        """
        Get author from database
        :param request:
        :param kwargs:
        :return:
        """
        pass

    def get_authors(self, request, **kwargs):
        """
        Get authors from database
        :param request:
        :param kwargs:
        :return:
        """
        pass

    def update_author(self, request, **kwargs):
        """
        update author from database
        :param request:
        :param kwargs:
        :return:
        """
        pass

    def delete_author(self, request, **kwargs):
        """
        update author from database
        :param request:
        :param kwargs:
        :return:
        """
        pass

    # Category CRUD
    def create_category(self, request, **kwargs):
        """
        Add authors to the database
        :param request:
        :param kwargs:
        :return:
        """
        pass

    def get_category(self, request, **kwargs):
        """
        Get author from database
        :param request:
        :param kwargs:
        :return:
        """
        pass

    def get_categories(self, request, **kwargs):
        """
        Get authors from database
        :param request:
        :param kwargs:
        :return:
        """
        pass

    def update_category(self, request, **kwargs):
        """
        update author from database
        :param request:
        :param kwargs:
        :return:
        """
        pass

    def delete_category(self, request, **kwargs):
        """
        update author from database
        :param request:
        :param kwargs:
        :return:
        """
        pass

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
                return {'code': '700.500.500', 'message': 'Transaction Failed'}
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
        pass

    def get_books(self, request, **kwargs):
        """
        Handles fetching of multiple books, either with added conditions
        (like active books or archived books etc.) or without conditions
        :param request: original request received 
        :param kwargs: The parameters used to filter based on conditions if any.
        :return: dict response of a list of all books based on conditions provided
        """
        pass

    def update_book(self, request, book_id, **kwargs):
        """
        Handles updating of books personal information or 
        any other information related to books
        :param request: Original Django HTTP request
        :type request: WSGIRequest
        :param book_id: 
        :param kwargs: dict of other parameters 
        :return: dict response
        """
        pass

    def delete_book(self, request, book_id):
        """
        Handles deletion of a book from the system hypothetically
        though the book is never deleted just updated to state deleted
        :param request: Original Django HTTP request
        :param book_id: the unique book identifier
        :return: dict response with code
        """
        pass

    def archive_book(self, request, book_id):
        """
        Handles archiving  of a book from the system, i.e. updated to state archived
        :param request: Original Django HTTP request
        :param book_id: the unique book identifier
        :return: dict response with code
        """
        pass
