from django.contrib.auth.models import User, Group
from rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_extensions.cache.mixins import CacheResponseMixin

from tutorial.quickstart.serializers import *
from tutorial.quickstart.models import Post, Comment, Category, MyUser
from tutorial.quickstart.tasks import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MyUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class PostView(CacheResponseMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows post to be viewed, added, edited and deleted
    """
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content", "=author__username"]
    ordering_fields = ['title']
    ordering = ['-id']

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class CommentView(CacheResponseMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows comment to be viewed, added, edited and deleted
    """
    permission_classes = (AllowAny,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["text", "=author__username"]
    ordering_fields = ['text']


class CategoryView(CacheResponseMixin, viewsets.ModelViewSet):
    """
       API endpoint that allows category to be viewed, added, edited and deleted
    """
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ['name']
    ordering = ['-id']


class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
