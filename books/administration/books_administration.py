class BooksAdministration(object):
    """
    handle the administration functionality relating to Books including CRUD
    """

    def create_book(self, request, **kwargs):
        """
          Handles adding of books in the library system
          :param request: the original request
          :param kwargs: keyword arguments for creation of book.
          :return: dict response with code 
          """
        author_id = kwargs.pop('author')
        category_id = kwargs.pop('category')

        print(kwargs)
        return {'code': '100.000.000', 'message': 'success'}

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
