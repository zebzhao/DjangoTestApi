import csv
import datetime

from django.core.management.base import BaseCommand
from django.db import models

from api.models import Property


class Command(BaseCommand):
    help = 'Import a csv file to the properties table'
    date_format = '%m/%d/%Y'
    # Extract out field names for date and integer fields for data cleaning
    date_fields = list(f.name for f in Property._meta.fields if isinstance(f, models.DateField))
    integer_fields = list(f.name for f in Property._meta.fields if isinstance(f, models.IntegerField))

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        path = options['path'].pop()
        with open(path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                Command.clean_data(row)
                _, created = Property.objects.get_or_create(**row)
            self.stdout.write(self.style.SUCCESS('Successfully imported file "%s"' % path))

    @staticmethod
    def clean_data(row):
        # Convert any empty fields into None
        for field in row:
            if len(row[field]) == 0:
                row[field] = None
        # Convert date fields into date objects
        for field in Command.date_fields:
            if row[field] is not None:
                row[field] = datetime.datetime.strptime(row[field], Command.date_format)
        # Convert date fields into date objects
        for field in Command.integer_fields:
            if row[field] is not None:
                row[field] = float(row[field])
