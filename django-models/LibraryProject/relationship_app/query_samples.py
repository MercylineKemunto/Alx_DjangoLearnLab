import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library

def books_by_author(author_name):
    """Fetch all books written by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
        return list(Book.objects.filter(author=author).values('title', 'publication_year'))
    except Author.DoesNotExist:
        return f"No books found for author: {author_name}"

def books_in_library(library_name):
    """Fetch all books available in a specific library."""
    try:
        library = Library.objects.get(name=library_name)
        return list(library.books.all().values('title', 'author__name', 'publication_year'))
    except Library.DoesNotExist:
        return f"Library '{library_name}' does not exist."

if __name__ == "__main__":
    print("Books by George Orwell:", books_by_author("George Orwell"))
    print("Books in Central Library:", books_in_library("Central Library"))

