import pytest
from mixer.backend.django import mixer

from books.backend.service import AuthorService, CategoryService, BookService, BookIssuedService

pytestmark = pytest.mark.django_db


@pytestmark
class TestAuthorService(object):
    """
     Test the Author  services
    """

    def test_get(self):
        mixer.blend('base.State', name="Active")
        mixer.blend('books.Author', first_name="John", last_name="Kayumba")
        author = AuthorService().get(first_name='John')
        assert author is not None, 'Should have a Author object'

    def test_filter(self):
        """ Test for filter Author Model  service"""
        mixer.blend('base.State', name="Active")
        mixer.cycle(4).blend('books.Author')
        authors = AuthorService().filter()
        assert authors is not None, 'Should return a queryset of Authors'
        assert len(authors) == 4, 'should return four Authors'

    def test_create(self):
        """ Test for create Author Model service """
        mixer.blend('base.State', name="Active")
        kwargs = {
            'first_name': "John",
            'last_name':"Sakaja",
            'description': 'the renowned writter of playbook',
            'salutation': 'Mrs',
            'state': mixer.blend('base.State', name='Active')

        }
        author = AuthorService().create(**kwargs)
        assert author is not None, 'should return created Author object'

    def test_update(self):
        mixer.blend('base.State', name="Active")
        mixer.blend('books.Author')
        old_author = mixer.blend('books.Author', name="John Sakaja")
        new_author = AuthorService().update(old_author.id, name='JohnStone Sakaja')
        assert new_author.name == 'JohnStone Sakaja', 'Should have an updated instance of Author'


@pytestmark
class TestCategoryService(object):
    """
     Test the Category Model services
    """

    def test_get(self):
        mixer.blend('base.State', name="Active")
        mixer.blend('books.Category', name='Fiction')
        category = CategoryService().get(name='Fiction')
        assert category is not None, 'Should have a Category object'

    def test_filter(self):
        """ Test for filter category service"""
        mixer.blend('base.State', name='Active')
        mixer.cycle(4).blend('books.Category')
        category = CategoryService().filter()
        assert category is not None, 'Should return a queryset of Category'
        assert len(category) == 4, 'should return four Category instances'

    def test_create(self):
        """ Test for create Category service """
        mixer.blend('base.State', name='Active')
        category = CategoryService().create(name="Fiction", description="Best seller of the year")
        assert category is not None, 'should return created Category  object'

    def test_update(self):
        mixer.blend('base.State', name='Active')
        old_category = mixer.blend('books.Category', name="Fiction")
        new_category = CategoryService().update(old_category.id, name='Science Fiction')
        assert new_category.name == 'Science Fiction', 'Should have an updated instance of State'


@pytestmark
class TestBookService(object):
    """
     Test the Books Model services
    """

    def test_get(self):
        mixer.blend('base.State', name="Active")
        mixer.blend('books.Books', title="New Mahattan")
        book = BookService().get(title='New Mahattan')
        assert book is not None, 'Should have a Book object'

    def test_filter(self):
        """ Test for filter Book service"""
        mixer.blend('base.State', name="Active")
        mixer.cycle(4).blend('books.Books')
        books = BookService().filter()
        assert books is not None, 'Should return a queryset of books'
        assert len(books) == 4, 'should return four books'

    def test_create(self):
        """ Test for create Book service """
        mixer.blend('base.State', name="Active")
        kwargs = {
            "title": "New Yorks Rocks",
            'published_date': "2023-04-01",
            'edition': '1st edition',
            'ISBN': '4477858494999F484',
            'author': mixer.blend('books.Author'),
            'category': mixer.blend('books.Category')
        }
        book = BookService().create(**kwargs)
        assert book is not None, 'should return created Book object'

    def test_update(self):
        mixer.blend('base.State', name="Active")
        old_book = mixer.blend('books.Books', title="The Titans")
        update_book = BookService().update(old_book.id, title='The titans and Others')
        assert old_book.title is not update_book.title, 'Should have an updated instance of Book'


@pytestmark
class TestBookIssuedService(object):
    """
     Test the BookIssued Model services
    """

    def test_get(self):
        mixer.blend('base.State', name="Active")
        book = mixer.blend('books.Books', title='Frictionless')
        member = mixer.blend('members.Members')
        mixer.blend('books.BookIssued', book=book, member=member)
        book_issued = BookIssuedService().get(book__title=book.title)
        assert book_issued is not None, 'Should have a BookIssued object'

    def test_filter(self):
        """ Test for filter BookIssued service"""
        mixer.blend('base.State', name="Active")
        mixer.cycle(4).blend('books.BookIssued')
        book_issued = BookIssuedService().filter()
        assert book_issued is not None, 'Should return a queryset of BookIssued'
        assert len(book_issued) == 4, 'should return four BookIssued'

    def test_create(self):
        """ Test for create BookIssued service """
        mixer.blend('base.State', name="Active")
        kwargs = {
            'book': mixer.blend('books.Books'),
            'member': mixer.blend('members.Members'),
            'borrow_duration': 20,
            'return_date': '2023-05-05',
            'return_fee': 150,
        }
        book_issued = BookIssuedService().create(**kwargs)
        assert book_issued is not None, 'should return created BookIssued object'

    def test_update(self):
        mixer.blend('base.State', name="Active")
        book = mixer.blend('books.Books', title='Frictionless')
        book2 = mixer.blend('books.Books', title='Frictionless Birds')
        member = mixer.blend('members.Members')
        book_issued = mixer.blend('books.BookIssued', book=book, member=member)
        updated_book_issued = BookIssuedService().update(book_issued.id, book=book2)
        assert updated_book_issued.book.title == 'Frictionless Birds', 'Should have an updated instance of BookIssued'
