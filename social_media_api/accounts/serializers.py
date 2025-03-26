from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        """Create a new user with a hashed password and generate a token"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),  # Optional email
            password=validated_data['password']
        )
        Token.objects.create(user=user)  # Create an authentication token for the user
        return user
