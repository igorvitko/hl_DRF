import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
# from django.test import TestCase

from tutorial.quickstart.models import Post, Category, Comment
from tutorial.quickstart.serializers import *


# initialize the APIClient app
client = APIClient()


class PostTest(APITestCase):
    """ test module for create post, get postlist, create comment"""

    def setUp(self):
        self.test_user = MyUser.objects.create_user(username='ihor', password='pass1234')
        self.test_user_token = Token.objects.create(user=self.test_user)

        self.test_category = Category.objects.create(
            name='Статья', slug='statya')

        self.valid_post = {
            'title': "Test Post",
            'slug': 'test-post',
            'author': 1,
            'content': "Something about tests",
            'category': 1,
        }

        self.invalid_post = {
            'title': "",
            'slug': 'test-post_2',
            'author': 1,
            'content': "Something about tests",
            'category': 1,
        }

        Post.objects.create(
            title="Test test Post",
            slug='test-test-post',
            author=self.test_user,
            content="Something about all test",
            category=self.test_category,
        )

    def test_create_valid_post(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token.key)

        response = client.post(
            '/api/v1/post/',
            data=json.dumps(self.valid_post),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_create_invalid_post(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token.key)

        response = client.post(
            '/api/v1/post/',
            data=json.dumps(self.invalid_post),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 1)

    def test_get_all_posts(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token.key)

        response = client.get('/api/v1/post/')
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data["results"], serializer.data)
        # self.assertEqual(Post.objects.count(), 1)

    def test_create_comment(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token.key)

        data_comment = {
                "text": "Very good!",
                "post": 1,
                "author": 1
            }
        response = client.post(
            '/api/v1/comment/',
            data_comment,
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Post.objects.get(pk=1).post_comments.count(), 1)
        self.assertEqual(Post.objects.get(pk=1).post_comments.get(pk=1).text, "Very good!")

