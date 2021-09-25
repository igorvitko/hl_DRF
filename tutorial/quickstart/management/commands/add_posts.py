from django.core.management.base import BaseCommand
from django.utils.text import slugify

from faker import Faker
from random import randint

from tutorial.quickstart.models import *


class Command(BaseCommand):
    help = 'Adding posts in blog'

    def add_arguments(self, parser):
        parser.add_argument('-q', '--quantity', type=int, default=10, help="enter needs quantity of posts")

    def handle(self, *args, **options):
        fake = Faker(['ru-RU', 'en-US'])

        authors = MyUser.objects.all()

        self.stdout.write('Start inserting posts...')
        for _ in range(options['quantity']):

            if authors.count() == 0:
                author = MyUser(username='test', password='test12345', email='test@tutorial.com')
                author.save()
                author = MyUser.objects.get(pk=1)
            else:
                quantity_authors = authors.count()
                author = MyUser.objects.get(pk=randint(1, quantity_authors))

            category = Category.objects.get(pk=1)

            if not category:
                category = Category(name='test_category', slug="test-cat")
                category.save()
                category = Category.objects.get(pk=1)

            post = Post(author=author, category=category)
            post.title = fake['ru-RU'].sentence(nb_words=randint(3, 7), variable_nb_words=True)
            post.slug = slugify(fake['en-US'].sentence(nb_words=3, variable_nb_words=True).replace(".", ""))
            post.content = fake['ru-RU'].text(max_nb_chars=200)

            post.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully inserted {options['quantity']} posts"))
