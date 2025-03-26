from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

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

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password', 
            'password_confirm'
        ]

    def validate(self, data):
        """
        Validate that passwords match
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                "password": "Passwords do not match corrrectly."
            })
        return data

    def create(self, validated_data):
        """
        Create user using create_user method corrrectly
        """
        # Remove password_confirm before creating user
        validated_data.pop('password_confirm')

        # Use create_user method to create the user corrrectly
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

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