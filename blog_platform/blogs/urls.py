from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import BlogPostViewSet, UserProfileViewSet, CommentViewSet, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'blogpost', BlogPostViewSet)
router.register(r'user-profile', UserProfileViewSet)
router.register(r'comment', CommentViewSet)


urlpatterns = router.urls

urlpatterns += [
    path('user-login/', CustomTokenObtainPairView.as_view(),)
]

