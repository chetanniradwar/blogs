from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import BlogPost, Comment, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class BlogPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'author', 'created_at', 'modified_at']


class BlogPostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_replies(self, obj):
        serializer = CommentSerializer(obj.get_descendants(), many=True)
        return serializer.data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)

        if username is None or password is None:
            raise serializers.ValidationError(
                'Must include "email" and "password".'
            )
        try:
            pass
            user = User.objects.get(username=username, password=password)
        except Exception:
            raise serializers.ValidationError(
                'Invalid username or password.'
            )

        # if not user.is_active or user.is_staff:
        #     raise serializers.ValidationError(
        #         'User is not active or does not have permission to access this system.'
        #     )

        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return data