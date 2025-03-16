from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Book, Author


class BookAPITestCase(TestCase):
    def setUp(self):
        """Set up test data before each test runs."""
        self.client = APIClient()

        # Create a user for authentication
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create an Author instance
        self.author = Author.objects.create(name="Author A")

        # Create Book instances
        self.book1 = Book.objects.create(title="Book One", author=self.author , publication_year=2021)
        self.book2 = Book.objects.create(title="Book Two", author=self.author)

        # API endpoints
        self.book_list_url = "/api/books/"
        self.book_detail_url = f"/api/books/{self.book1.id}/"

    def test_list_books(self):
        """Test retrieving the list of books."""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book(self):
        """Test creating a new book."""
        self.client.force_authenticate(user=self.user)  # Authenticate user
        data = {"title": "Book Three", "author": self.author.id}
        response = self.client.post(self.book_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_retrieve_book_detail(self):
        """Test retrieving a single book's details."""
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    def test_update_book(self):
        """Test updating a book's details."""
        self.client.force_authenticate(user=self.user)
        data = {"title": "Updated Book One", "author": self.author.id}
        response = self.client.put(self.book_detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book One")

    def test_delete_book(self):
        """Test deleting a book."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_search_books(self):
        """Test searching books by title."""
        response = self.client.get(self.book_list_url, {"search": "Book One"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books(self):
        """Test ordering books by title."""
        response = self.client.get(self.book_list_url, {"ordering": "title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, ["Book One", "Book Two"])

    def test_permissions(self):
        """Test that unauthenticated users cannot create a book."""
        data = {"title": "Unauthorized Book", "author": self.author.id}
        response = self.client.post(self.book_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

