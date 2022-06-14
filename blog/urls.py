from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap
from .views import CreatePostAPIView, GetPostListAPIView, PostLikeAPIView, PostUnlikeAPIView, PostLikeUnlikeAPIView, \
    AnalyticsAPIView, UserAnaliticAPIView, GetPostAPIView

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('', GetPostListAPIView.as_view(), name='all-posts'),
    path('get-post/<str:pk>/', GetPostAPIView.as_view(), name='get-post'),
    path('create-post/', CreatePostAPIView.as_view(), name='create-post'),
    path('like-post/<str:pk>/', PostLikeAPIView.as_view(), name='like-post'),
    path('unlike-post/<str:pk>/', PostUnlikeAPIView.as_view(), name='unlike-post'),
    path('like-unlike-post/<str:pk>/', PostLikeUnlikeAPIView.as_view(), name='like-unlike-post'),
    path('analytic/', AnalyticsAPIView.as_view(), name='analytic'),
    path('user-analytic/<str:pk>/', UserAnaliticAPIView.as_view(), name='user-analytic'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
]
