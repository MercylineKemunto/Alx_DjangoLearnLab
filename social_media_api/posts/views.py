from django.shortcuts import render

# posts/views.py
from rest_framework import viewsets, permissions
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit it
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    """
    Viewset for Post model with additional actions
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # Optional: Add filtering capabilities
        queryset = Post.objects.all()
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset

    @action(detail=True, methods=['post'])
    def add_comment(self, request, slug=None):
        """
        Custom action to add a comment to a specific post
        """
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(
                post=post, 
                author=request.user
            )
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset for Comment model
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
