# Django REST Framework: Models and Serializers Documentation

## Overview
This document provides a detailed explanation of the **Author** and **Book** models, their relationships, and the custom serializers implemented for efficient data handling in Django REST Framework (DRF).

---

## 1. Models

### **Author Model**
```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
```
#### **Description**:
- Represents an author in the system.
- Contains a single field `name` to store the author's name.
- The `__str__` method returns the author's name for easy identification.

---

### **Book Model**
```python
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
```
#### **Description**:
- Represents a book with three fields:
  - `title`: The book’s title.
  - `publication_year`: The year the book was published.
  - `author`: A ForeignKey linking the book to an `Author` (one-to-many relationship).
- The `related_name="books"` in the ForeignKey allows us to access all books by an author using `author.books.all()`.
- The `__str__` method returns the book title for better readability.

---

## 2. Serializers

### **BookSerializer**
```python
from rest_framework import serializers
from .models import Book
import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        if value > datetime.datetime.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value
```
#### **Description**:
- Serializes all fields of the `Book` model.
- Implements **custom validation** for `publication_year` to prevent future dates.

---

### **AuthorSerializer**
```python
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
```
#### **Description**:
- Serializes the `Author` model.
- Uses **nested serialization** to include all related books within an author’s data.
- The `books` field is **read-only** to prevent modifying books directly from the author serializer.

---

## 3. Relationships & Data Flow
- **One-to-Many Relationship**: Each `Author` can have multiple `Book` entries.
- **Nested Serialization**: The `AuthorSerializer` includes all related books in its output.
- **Validation**: Ensures `publication_year` does not exceed the current year.

---

## 4. Testing the Serializers
### **Django Shell Testing**
```python
python manage.py shell
```
```python
from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer

# Create Author
author = Author.objects.create(name="J.K. Rowling")

# Create Book
book = Book.objects.create(title="Harry Potter", publication_year=2000, author=author)

# Serialize Author Data
author_data = AuthorSerializer(author).data
print(author_data)  # {'name': 'J.K. Rowling', 'books': [{'title': 'Harry Potter', 'publication_year': 2000, 'author': 1}]}
```

---

## 5. Conclusion
This documentation provides an overview of the `Author` and `Book` models, their relationships, and their corresponding serializers. The nested serialization and validation techniques help maintain data integrity and improve API response structure.

For further enhancements, consider adding more custom fields or implementing additional serializer methods.

