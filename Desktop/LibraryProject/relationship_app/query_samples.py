import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django-models.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# 1️⃣ Query all books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = author.books.all()
    return books

# 2️⃣ List all books in a library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

# 3️⃣ Retrieve the librarian for a library
def librarian_of_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian

# Example usage:
if __name__ == "__main__":
    print("Books by George Orwell:", books_by_author("George Orwell"))
    print("Books in City Library:", books_in_library("City Library"))
    print("Librarian of Central Library:", librarian_of_library("Central Library"))
