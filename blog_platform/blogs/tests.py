import json

import pytest
from django.contrib.auth.models import User
from django_dynamic_fixture import G
from rest_framework import status
from rest_framework.test import force_authenticate

from .models import UserProfile, BlogPost

from .views import UserProfileViewSet, BlogPostViewSet


@pytest.mark.usefixtures("request_factory")
class TestUserProfileViewSet:
    @pytest.mark.django_db
    def test_create_user_profile(self, request_factory):
        data = {
            "username": "login",
            "email": "login@admin.com",
            "password": "login",
            "name": "my name",
            "bio": "my username is login"
        }
        endpoint = '/user-profile/'
        data = json.dumps(data)
        request = request_factory.post(endpoint, data, content_type='application/json')
        view = UserProfileViewSet.as_view({'post': 'create'})

        response = view(request)

        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert UserProfile.objects.count() == 1
        assert User.objects.count() == 1

    @pytest.mark.django_db(transaction=True)
    def test_create_user_profile_with_existing_username(self, request_factory):
        user = G(UserProfile, user__username='login')
        data = {
            "username": "login",
            "email": "login@admin.com",
            "password": "login",
            "name": "my name",
            "bio": "my username is login"
        }

        endpoint = '/user-profile/'
        data = json.dumps(data)
        request = request_factory.post(endpoint, data, content_type='application/json')
        view = UserProfileViewSet.as_view({'post': 'create'})

        response = view(request)
        assert response.status_code == 400
        assert UserProfile.objects.count() == 1
        assert User.objects.count() == 1


@pytest.mark.django_db
class TestBlogPostViewSet:
    def test_1_search_blog_posts(self, request_factory):
        G(BlogPost, keywords=['python', 'django'])
        G(BlogPost, keywords=['python', 'javascript'])

        endpoint = '/blog-post/search/?keywords=python,django'
        request = request_factory.get(endpoint, content_type='application/json')

        view = BlogPostViewSet.as_view({'get': 'search'})
        response = view(request)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['id'] == 1

    def test_2_search_blog_posts(self, request_factory):
        G(BlogPost, keywords=['python', 'django'])
        G(BlogPost, keywords=['python', 'javascript'])

        endpoint = '/blog-post/search/?keywords=python'
        request = request_factory.get(endpoint, content_type='application/json')

        view = BlogPostViewSet.as_view({'get': 'search'})
        response = view(request)

        assert response.status_code == 200
        assert len(response.data) == 2

    def test_like_blog_post(self, request_factory):
        user = G(User)
        blog_post = G(BlogPost)
        request = request_factory.patch(f'/blog-post/{blog_post.id}/like/', {'user': user.id},
                                        content_type='application/json')

        view = BlogPostViewSet.as_view({'patch': 'like'})
        force_authenticate(request, user=user)
        response = view(request, pk=blog_post.id)

        assert response.status_code == 200
        assert blog_post.likes.count() == 1

    def test_like_blog_post_already_liked(self, request_factory):
        user = G(User)
        blog_post = G(BlogPost , likes=[user])
        request = request_factory.patch(f'/blog-post/{blog_post.id}/like/', {'user': user.id},
                                        content_type='application/json')

        view = BlogPostViewSet.as_view({'patch': 'like'})
        force_authenticate(request, user=user)
        response = view(request, pk=blog_post.id)

        assert response.status_code == 400
        assert blog_post.likes.count() == 1

