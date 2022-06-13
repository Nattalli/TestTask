from rest_framework import serializers
from .models import Post, Like
from django.contrib.auth import get_user_model
User = get_user_model()


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('owner', 'title', 'content', 'image')


class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(PostListSerializer, self).to_representation(instance)
        rep['likes'] = Like.objects.filter(post_id=instance.id).count()
        return rep


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('post', 'user')
