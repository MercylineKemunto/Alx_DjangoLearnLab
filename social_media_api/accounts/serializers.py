from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token

# Ensure we're using the custom user model
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Explicit CharField for username
    username = serializers.CharField(
        required=True,
        max_length=150,
        min_length=3,
        error_messages={
            'required': 'Username is required',
            'max_length': 'Username must be no more than 150 characters',
            'min_length': 'Username must be at least 3 characters'
        }
    )

    # Explicit CharField for email
    email = serializers.CharField(
        required=True,
        max_length=254,
        error_messages={
            'required': 'Email is required',
            'max_length': 'Email must be no more than 254 characters'
        }
    )

    # Explicit CharField for passwords
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'},
        max_length=128,
        min_length=8,
        error_messages={
            'required': 'Password is required',
            'max_length': 'Password must be no more than 128 characters',
            'min_length': 'Password must be at least 8 characters'
        }
    )

    password_confirm = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'},
        max_length=128,
        min_length=8,
        error_messages={
            'required': 'Password confirmation is required',
            'max_length': 'Password confirmation must be no more than 128 characters',
            'min_length': 'Password confirmation must be at least 8 characters'
        }
    )

    # Token field
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password', 
            'password_confirm',
            'token'
        ]

    def validate(self, data):
        """
        Validate that passwords match
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                "password": "Passwords do not match."
            })
        return data

    def create(self, validated_data):
        """
        Create user and generate authentication token
        """
        # Remove password_confirm before creating user
        validated_data.pop('password_confirm')

        # Create user using create_user method
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Create a token for the user
        token = Token.objects.create(user=user)

        # Attach the token to the user instance for serializer response
        user.token = token.key

        return user

class UserProfileSerializer(serializers.ModelSerializer):
    # Explicit CharField for username in profile
    username = serializers.CharField(
        read_only=True,
        max_length=150
    )

    # Explicit CharField for email in profile
    email = serializers.CharField(
        read_only=True,
        max_length=254
    )

    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email'
        ]
        read_only_fields = ['id']