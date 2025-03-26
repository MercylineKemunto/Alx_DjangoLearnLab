from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
# Import Token model
from rest_framework.authtoken.models import Token

# Ensure we're using the custom user model
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Add CharField for passwords
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )
    # Add a token field to return the authentication token
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
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email'
        ]
        read_only_fields = ['id']