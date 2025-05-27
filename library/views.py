from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from library.serializers import RegisterSerializer, BookSerializer, LoanSerializer
from library.permissions import IsAdminOrReadOnly
from library.models import Book, Loan

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Book.objects.all().order_by('id')  # or 'title' or any field
        author = self.request.query_params.get('author')
        title = self.request.query_params.get('title')
        available = self.request.query_params.get('available')

        if author:
            queryset = queryset.filter(author__icontains=author)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if available is not None:
            queryset = queryset.filter(available=(available.lower() == 'true'))

        return queryset


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]


class BorrowBookView(generics.CreateAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        if not book_id:
            return Response({'error': 'Book ID is required.'}, status=400)

        try:
            book = Book.objects.get(id=book_id, available=True)
        except Book.DoesNotExist:
            return Response({'error': 'Book not available.'}, status=404)

        # Mark book unavailable & create loan
        book.available = False
        book.save()
        loan = Loan.objects.create(user=request.user, book=book)
        return Response(LoanSerializer(loan).data, status=201)


class ReturnBookView(generics.UpdateAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            loan = Loan.objects.get(
                user=request.user, book_id=request.data['book'], returned_at__isnull=True)
        except Loan.DoesNotExist:
            return Response({'error': 'Active loan not found.'}, status=404)

        loan.returned_at = timezone.now()
        loan.book.available = True
        loan.book.save()
        loan.save()
        return Response(LoanSerializer(loan).data)
