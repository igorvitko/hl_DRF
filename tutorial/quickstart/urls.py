# from django.urls import path, include
from rest_framework import routers

from tutorial.quickstart.views import *

router = routers.DefaultRouter()
router.register(r'post', PostView, basename='post')
router.register(r'comment', CommentView)
router.register(r'category', CategoryView)


urlpatterns = router.urls
