import logging

import django.contrib.auth
from django.core.management import BaseCommand
from backend.users.importers import ProfileImporter
from pathlib import Path

logger = logging.getLogger(__name__)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logger.addHandler(console)
logger.setLevel(logging.DEBUG)


class Command(BaseCommand):
    help = "Import user profiles into constallte "

    def handle(self, *args, **kwargs):
        importer = ProfileImporter()
        csv_path = Path() / "cats.csv"

        importer.load_csv(csv_path)
        first_row = importer.rows[1]

        logger.debug(f"importing: {first_row}")
        users = importer.create_users(importer.rows)
        logger.debug(f"imported: {users}")
        # logger.debug(f"No of profiles to import: {len(importer.rows)}")
        # logger.debug(f"No of profiles to import: {len(importer.rows)}")

