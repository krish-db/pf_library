from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from ..models import Book, Loan
from django.contrib.auth import get_user_model

User = get_user_model()

class BookListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="testpass")
        self.token = self.client.post(reverse('token_obtain_pair'), {
            "username": "user", "password": "testpass"
        }).data['access']
        Book.objects.create(title="Book1", author="A", isbn="111", page_count=100)

    def test_book_list_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.get(reverse('book-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class BorrowReturnBookTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="testpass")
        self.token = self.client.post(reverse('token_obtain_pair'), {
            "username": "user1", "password": "testpass"
        }).data["access"]

        self.book = Book.objects.create(
            title="Borrowable Book",
            author="Author",
            isbn="1234567890123",
            page_count=200,
            available=True
        )

    def test_borrow_book_successfully(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.post(reverse('borrow-book'), {"book": self.book.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertFalse(self.book.available)
        self.assertEqual(Loan.objects.count(), 1)
    
    def test_return_book_successfully(self):
        # Borrow the book first
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.client.post(reverse('borrow-book'), {"book": self.book.id})

        # Now return the book
        response = self.client.put(reverse('return-book'), {"book": self.book.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        loan = Loan.objects.get(book=self.book, user=self.user)
        self.book.refresh_from_db()
        self.assertIsNotNone(loan.returned_at)
        self.assertTrue(self.book.available)
