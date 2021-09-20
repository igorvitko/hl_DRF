from rest_framework.test import APIClient, APITestCase

from tutorial.quickstart.tasks import *


class TaskTest(APITestCase):
    """ test module for celery tasks"""

    def setUp(self):
        self.test_user = MyUser.objects.create_user(username='ihor', password='pass1234')
        self.test_user = MyUser.objects.create_user(username='ivan', password='pass1234')

    def test_task_change_status_users_false_to_true(self):
        self.task_status_false = change_user_status()
        self.assertEqual(MyUser.objects.get(pk=2).is_notified, True)

    def test_task_change_status_users_true_to_false(self):
        self.task_status_false = change_user_status(True)
        self.assertEqual(MyUser.objects.get(pk=1).is_notified, False)
