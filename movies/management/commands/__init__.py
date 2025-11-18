# app1/management/commands/import_csv_data.py

import csv
from django.core.management.base import BaseCommand
from links.models import Link
from movies.models import Movie
from ratings.models import Rating
from tags.models import Tag

class Command(BaseCommand):
    help = "Import data from CSV files into corresponding models"

    def handle(self, *args, **options):
        self.import_file('data/movies.csv', Movie)
        self.import_file('data/tags.csv', Tag)
        self.import_file('data/ratings.csv', Rating)
        self.import_file('data/links.csv', Link)
        self.stdout.write(self.style.SUCCESS("✅ All CSV data imported successfully!"))

    def import_file(self, filepath, model):
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # model.objects.all().delete()  # optional: clear old data

            for row in reader:
                # create instance using unpacked dictionary
                model.objects.create(**row)

        self.stdout.write(f"Imported {filepath} → {model.__name__}")
