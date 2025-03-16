from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters import rest_framework as filters

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorViewSet(ModelViewSet):
    """
    API endpoint that allows authors to be viewed, created, updated, or deleted.
    - Read access is available to unauthenticated users.
    - Write access (create, update, delete) is restricted to authenticated users.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['name']  # Example filtering by author's name

class BookViewSet(ModelViewSet):
    """
    API endpoint that allows books to be viewed, created, updated, or deleted.
    - Read access is available to unauthenticated users.
    - Write access (create, update, delete) is restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['title', 'author']  # Example filtering by book title and author

class BookListView(generics.ListAPIView):
    """
    API endpoint to list books with filtering support.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['title', 'author']




