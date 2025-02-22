import os
import django

# Ensure Django is set up correctly
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book

# Ensure the author exists before querying
author, created = Author.objects.get_or_create(name="George Orwell")

# If created, print confirmation
if created:
    print(f"Added new author: {author.name}")
else:
    print(f"Author already exists: {author.name}")

# Ensure some books exist
book1, created1 = Book.objects.get_or_create(title="1984", author=author)
book2, created2 = Book.objects.get_or_create(title="Animal Farm", author=author)

if created1:
    print(f"Added book: {book1.title}")
if created2:
    print(f"Added book: {book2.title}")

# Fetch and print books by George Orwell
books = Book.objects.filter(author=author)
print("Books by George Orwell:", list(books))
