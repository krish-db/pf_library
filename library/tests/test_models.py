from django.test import TestCase
from ..models import Book

class BookModelTest(TestCase):
    def test_create_book(self):
        book = Book.objects.create(
            title="Test Book",
            author="Author A",
            isbn="1234567890123",
            page_count=300
        )
        self.assertEqual(str(book), "Test Book by Author A")
