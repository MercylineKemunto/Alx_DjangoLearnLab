from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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

class BookViewSet(ModelViewSet):
    """
    API endpoint that allows books to be viewed, created, updated, or deleted.
    - Read access is available to unauthenticated users.
    - Write access (create, update, delete) is restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AuthorListView(ListView):
    model = Author
    template_name = 'author_list.html'
    context_object_name = 'authors'

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'
    context_object_name = 'author'

class AuthorCreateView(CreateView):
    model = Author
    fields = ['name', 'bio']
    template_name = 'author_form.html'
    success_url = '/'  # Update as needed

class AuthorUpdateView(UpdateView):
    model = Author
    fields = ['name', 'bio']
    template_name = 'author_form.html'
    success_url = '/'  # Update as needed

class AuthorDeleteView(DeleteView):
    model = Author
    template_name = 'author_confirm_delete.html'
    success_url = '/'  # Update as needed



