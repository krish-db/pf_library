from django.test import TestCase
from ..models import Book
from ..serializers import BookSerializer

class BookSerializerTest(TestCase):
    def test_valid_serializer(self):
        data = {
            "title": "Test",
            "author": "Author A",
            "isbn": "1234567890123",
            "page_count": 100,
            "available": True
        }
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())
