"""
This to test books models module
"""
import datetime

import pytest
#
from mixer.backend.django import mixer

from books.models import Category, Author, Books

#
# # nonspection SpellCheckingInspection
#
pytestmark = pytest.mark.django_db


class TestBooksModels(object):
    """ Test cases for all models under books module"""

    def test_author(self):
        """ Test for Author model"""
        author = mixer.blend(
            'books.Author', salutation='Mr.', name="John Sakaja", state=mixer.blend('base.State', name="Active"))
        assert author is not None, 'Should return  Author instance'
        assert author.__str__() == f"{author.salutation} {author.name}", 'Should be Author string object representation'

    def test_category(self):
        """ Test for category model"""
        mixer.blend('base.State', name="Active")
        obj = mixer.blend('books.Category', name="Fiction")
        assert obj is not None, 'Should return a category instance'
        assert obj.__str__() == f"{obj.name}", "'Should be Category string object representation'"

    def test_books(self):
        """ Test for books model"""
        mixer.blend('base.State', name="Active")
        book = mixer.blend('books.Books', title="The Tears of a Cobra")
        assert book is not None, 'Should return books instance'
        assert book.__str__() == f"{book.title} - {book.author}", "'Should be Book string object representation'"

    def test_books_issued(self):
        """ Test for booksIssued model"""
        mixer.blend('base.State', name='Active')
        book = mixer.blend('books.Books', title="The Tears of a Cobra")
        member_issued = mixer.blend('members.Members')
        book_issued = mixer.blend('books.BookIssued', member=member_issued, book=book)
        assert book_issued is not None, 'Should return BookIssued instance'
        assert book_issued.__str__() == f"{book_issued.book} - {book_issued.member} - {book_issued.return_date}",\
            "'Should be BookIssued string object representation'"
