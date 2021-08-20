from django.contrib.auth.models import User, Group
from rest_framework import serializers

from tutorial.quickstart.models import Post, Comment, Category


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['slug', 'title', 'content', 'author', 'category']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created_on']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
