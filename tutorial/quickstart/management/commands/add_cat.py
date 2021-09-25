from django.core.management.base import BaseCommand
from django.utils.text import slugify
from transliterate import translit

from faker import Faker

from tutorial.quickstart.models import *


class Command(BaseCommand):
    help = 'Adding category in blog'

    def add_arguments(self, parser):
        parser.add_argument('-q', '--quantity', type=int, default=10, help="enter needs quantity of category")

    def handle(self, *args, **options):
        fake = Faker(['ru-RU'])

        self.stdout.write('Start inserting posts...')
        for _ in range(options['quantity']):
            category = Category(name=fake.sentence(nb_words=2, variable_nb_words=False).replace('.', ''))
            category.slug = slugify(translit(category.name, language_code='ru', reversed=True))

            category.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully inserted {options['quantity']} category"))
