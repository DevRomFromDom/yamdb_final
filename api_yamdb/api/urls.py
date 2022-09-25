from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet, MeAPIView,
                    ReviewViewSet, TitleViewSet, UserViewSet, create_token,
                    create_user)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(
    prefix='categories',
    viewset=CategoryViewSet,
    basename='categories',
)
router_v1.register(
    prefix='genres',
    viewset=GenreViewSet,
    basename='genres',
)
router_v1.register(
    prefix='titles',
    viewset=TitleViewSet,
    basename='titles',
)
router_v1.register(
    prefix=r'titles/(?P<title_id>\d+)/reviews',
    viewset=ReviewViewSet,
    basename='reviews',
)
router_v1.register(
    prefix=(r'titles/(?P<title_id>\d+)/'
            r'reviews/(?P<reviews>\d+)/comments'),
    viewset=CommentViewSet,
    basename='comments',
)
router_v1.register(
    prefix='users',
    viewset=UserViewSet,
    basename='users',
)

token_auth_urls = [
    path(
        'auth/token/',
        create_token,
        name='token_obtain_pair'
    ),
    path('auth/signup/', create_user, name='auth/signup')
]

urlpatterns = [
    re_path(
        r'(?P<version>v1)/users/me',
        MeAPIView.as_view(),
        name='users-me'
    ),
    re_path(r'(?P<version>v1)/', include(router_v1.urls)),
    path('v1/', include(token_auth_urls))
]
