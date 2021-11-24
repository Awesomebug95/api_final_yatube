from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.generics import get_object_or_404

from posts.models import Comment, Post, Follow, Group, User

CANT_SUBSCRIBE_URSELF = 'Нельзя подписаться самому на себя!'
ALREADY_FOLLOW = 'Вы уже подписаны на этого автора.'


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    def validate(self, data):
        user = get_object_or_404(User, username=data['following'].username)
        follow = Follow.objects.filter(
            user=self.context['request'].user,
            following=user
        )
        if user == self.context['request'].user:
            raise serializers.ValidationError(CANT_SUBSCRIBE_URSELF)
        if follow:
            raise serializers.ValidationError(ALREADY_FOLLOW)
        return data

    class Meta:
        model = Follow
        fields = ('user', 'following')
        read_only_fields = ('id', 'user')
