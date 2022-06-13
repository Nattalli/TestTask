from django.urls import path
from .views import CreatePostAPIView, GetPostListAPIView, PostLikeAPIView, PostUnlikeAPIView, PostLikeUnlikeAPIView, \
    AnalyticsAPIView, UserAnaliticAPIView


urlpatterns = [
    path('', GetPostListAPIView.as_view(), name='all-posts'),
    path('create-post/', CreatePostAPIView.as_view(), name='create-post'),
    path('like-post/<str:pk>/', PostLikeAPIView.as_view(), name='like-post'),
    path('unlike-post/<str:pk>/', PostUnlikeAPIView.as_view(), name='unlike-post'),
    path('like-unlike-post/<str:pk>/', PostLikeUnlikeAPIView.as_view(), name='like-unlike-post'),
    path('analytics/', AnalyticsAPIView.as_view(), name='analytic'),
    path('user-analytic/<str:pk>/', UserAnaliticAPIView.as_view(), name='user-analytic')
]
