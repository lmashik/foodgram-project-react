import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    """Management-команда для добавления ингредиентов в базу данных."""
    def handle(self, *args, **options):
        csv_path = os.path.join(
            settings.BASE_DIR,
            'data/ingredients.csv',
        )
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader:
                obj, created = Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                )
        print('Ingredients added from file to database.')
