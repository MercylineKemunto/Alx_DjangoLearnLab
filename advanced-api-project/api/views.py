from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from rest_framework import generics

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'

class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'author']
    template_name = 'books/book_form.html'

class BookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'author']
    template_name = 'books/book_form.html'

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'




