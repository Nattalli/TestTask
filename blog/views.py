from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from .models import Post, Like
from rest_framework.response import Response
from .serializers import PostSerializer, PostListSerializer, LikeSerializer
from TestTask.pagination import NewPagination

User = get_user_model()


class CreatePostAPIView(generics.CreateAPIView):
    """
    Creation of a new post. Allowed for authorised users only.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class GetPostListAPIView(generics.ListAPIView):
    """
    Return a list of all created posts.
    """
    serializer_class = PostListSerializer
    queryset = Post.objects.all().order_by('-id').prefetch_related('likes')
    pagination_class = NewPagination

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)


# the first solution, when the button to like and unlike are different
class PostLikeAPIView(generics.CreateAPIView):
    """
    Post like. Allowed for authorised users only. In the url sends post id.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        data = {
            'user': user_id,
            'post': kwargs['pk']
        }
        likes = Like.objects.filter(post_id=kwargs['pk'], user_id=user_id).count()
        if likes == 0:
            serializer = self.get_serializer(data=data, many=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"message": "You had already liked this post"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class PostUnlikeAPIView(generics.DestroyAPIView):
    """
    Post unlike. Allowed for authorised users only. In the url sends post id.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            instance = Like.objects.get(post_id=kwargs['pk'], user_id=request.user.id)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={'message': 'You did not like this post.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def perform_destroy(self, instance):
        instance.delete()


# the second solution, when like and unlike is the same button
class PostLikeUnlikeAPIView(generics.CreateAPIView):
    """
    Post like/unlike. Allowed for authorised users only. In the url sends post id.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = kwargs['pk']
        user_id = request.user.id
        instance = Like.objects.filter(post_id=post_id, user_id=user_id)
        if instance.count() == 0:
            try:
                like = Like.objects.create(post_id=post_id, user_id=user_id)
                return Response(data={'message': 'Liked successfully!'}, status=status.HTTP_201_CREATED)
            except:
                return Response(data={'message': 'Such post does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            Like.objects.get(post_id=post_id, user_id=user_id).delete()
            return Response(data={'message': 'Like successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
