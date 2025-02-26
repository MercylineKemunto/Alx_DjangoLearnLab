import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.filter(name=author_name).first()
    if author:
        return author.books.all()
    return []

# List all books in a specific library
def get_books_in_library(library_name):
    library = Library.objects.filter(name=library_name).first()
    if library:
        return library.books.all()
    return []

# Retrieve the librarian for a specific library
def get_librarian_for_library(library_name):
    library = Library.objects.filter(name=library_name).first()
    if library and hasattr(library, 'librarian'):
        return library.librarian
    return None

# Example usage
if __name__ == "__main__":
    print("Books by Author:", get_books_by_author("J.K. Rowling"))
    print("Books in Library:", get_books_in_library("City Library"))
    print("Librarian of Library:", get_librarian_for_library("City Library"))
