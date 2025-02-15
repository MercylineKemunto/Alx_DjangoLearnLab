# Retrieve Book

```python
from bookshelf.models import Book

# Retrieve all books
books = Book.objects.all()
print(books)  # Output should list all books
