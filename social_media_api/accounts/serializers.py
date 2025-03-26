from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password', 
            'password_confirm', 
            'bio', 
            'profile_picture',
            'token'
        ]
        extra_kwargs = {
            'bio': {'required': False},
            'profile_picture': {'required': False}
        }

    def validate(self, data):
        """
        Validate password matching and username uniqueness
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        # Check if username already exists
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "A user with this username already exists."})
        
        return data

    def create(self, validated_data):
        """
        Create user and generate authentication token
        """
        # Remove confirm password before creating user
        validated_data.pop('password_confirm')
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture')
        )
        
        # Generate token for the user
        Token.objects.create(user=user)
        
        return user

    def get_token(self, obj):
        """
        Retrieve user's authentication token
        """
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key

class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'bio', 
            'profile_picture', 
            'followers_count', 
            'following_count'
        ]
        read_only_fields = ['id', 'followers_count', 'following_count']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()