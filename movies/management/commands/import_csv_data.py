# movies/management/commands/import_csv_data.py

import csv
import os
from django.core.management.base import BaseCommand
from django.db import models
from movies.models import Movie
from links.models import Link
from ratings.models import Rating
from tags.models import Tag

class Command(BaseCommand):
    help = "Import data from CSV files into the corresponding models"

    def handle(self, *args, **options):
        base_path = os.path.join(os.getcwd(), 'data')  # folder where CSVs live

        files_and_models = [
            ('movies.csv', Movie),
            ('links.csv', Link),
            ('ratings.csv', Rating),
            ('tags.csv', Tag),
        ]

        for filename, model in files_and_models:
            filepath = os.path.join(base_path, filename)
            if not os.path.exists(filepath):
                self.stdout.write(self.style.WARNING(f"⚠️  File not found: {filepath}"))
                continue

            self.import_csv(filepath, model)
            self.stdout.write(self.style.SUCCESS(f"✅ Imported {filename} into {model.__name__}"))

        self.stdout.write(self.style.SUCCESS("🎉 All CSV imports finished!"))

    def import_csv(self, filepath, model):
        batch_size = 1000
        objects_to_create = []
        count = 0
        skipped = 0

        # detect foreign keys
        fk_fields = {f.name for f in model._meta.fields if isinstance(f, models.ForeignKey)}
        pk_field = model._meta.pk.name

        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cleaned = {}
                skip_row = False

                for key, value in row.items():
                    field_name = key + "_id" if key in fk_fields else key

                    # Skip empty numeric fields
                    try:
                        field = model._meta.get_field(field_name)
                    except Exception:
                        continue  # field not in model, skip

                    if value == '' and isinstance(field, (models.IntegerField, models.DecimalField, models.BigIntegerField)):
                        skip_row = True
                        break

                    # assign foreign keys with _id suffix
                    if key in fk_fields:
                        cleaned[key + "_id"] = value
                    else:
                        cleaned[key] = value

                if skip_row:
                    skipped += 1
                    continue

                # skip duplicates by primary key if it exists in row
                exists = model.objects.filter(**{pk_field: cleaned[pk_field]}).exists() if pk_field in cleaned else False
                if not exists:
                    objects_to_create.append(model(**cleaned))
                    count += 1

                    if count % batch_size == 0:
                        self.stdout.write(f"{count} rows prepared for {model.__name__}...")

            if objects_to_create:
                model.objects.bulk_create(objects_to_create)
                self.stdout.write(f"Inserted {len(objects_to_create)} rows into {model.__name__}")

            if skipped > 0:
                self.stdout.write(f"Skipped {skipped} invalid rows in {model.__name__}")
    