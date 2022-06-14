import datetime

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


class LikeAnalyticSerializer(serializers.Serializer):

    def to_representation(self, instance):
        rep = super(LikeAnalyticSerializer, self).to_representation(instance)

        date_from = datetime.datetime.strptime(instance['date_from'], '%Y-%m-%d').date()
        date_to = datetime.datetime.strptime(instance['date_to'], '%Y-%m-%d').date()
        queryset = Like.objects.filter(time__gte=date_from, time__lte=date_to)

        while date_from <= date_to:

            rep[str(date_from)] = {'qty': queryset.filter(time=date_from).count()}
            date_from += datetime.timedelta(days=1)

        return rep


class UserAnalyticSerializer(serializers.Serializer):

    activity = serializers.DateTimeField()
    login = serializers.DateTimeField()
