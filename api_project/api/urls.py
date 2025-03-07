from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookList

# Create a router and register the BookViewSet for CRUD operations
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

# Define urlpatterns for both ListAPIView and ViewSet
urlpatterns = [
    # Route for listing books using ListAPIView
    path('books/', BookList.as_view(), name='book-list'),

    # Include the router-generated URLs for full CRUD operations
    path('', include(router.urls)),
]
