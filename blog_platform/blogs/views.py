
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import *
from .serializers import BlogPostListSerializer, BlogPostDetailSerializer, CommentSerializer, UserProfileSerializer, \
    CustomTokenObtainPairSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        user_obj = None
        try:
            user_obj = User.objects.create(username=username, email=email, password=password)

            request_data = request.data
            request_data.pop("username")
            request_data.pop("email")
            request_data.pop("password")
            request_data.update({"user": user_obj.id})

            serialized_data = UserProfileSerializer(data=request_data)
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save()

        except Exception as e:
            if user_obj:
                user_obj.delete()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "user created"}, status=status.HTTP_201_CREATED)


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostDetailSerializer

    def get_permissions(self):
        if self.action in ['list', 'search']:
            return []
        return super().get_permissions()

    @action(methods=['get'], detail=False)
    def search(self, request, *args, **kwargs):
        keywords = request.query_params.get('keywords')

        keywords = keywords.split(',')
        queryset = self.queryset.filter(keywords__contains=keywords)

        data = BlogPostListSerializer(queryset, many=True).data

        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True)
    def like(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        try:
            blog_obj = BlogPost.objects.get(id=pk)
        except Exception:
            return Response({"error": "post does not exits"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.data.get('user')

        if user_id in blog_obj.likes.all().values_list('id', flat=True):
            return Response({"error": "already liked"}, status=status.HTTP_400_BAD_REQUEST)

        blog_obj.likes.add(user_id)

        blog_obj.save()

        return Response({"message": "success"}, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent_comment__isnull=True)
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    # authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return []
        return super().get_permissions()

    filterset_fields = {
        'blog_post': ['exact']
    }


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
