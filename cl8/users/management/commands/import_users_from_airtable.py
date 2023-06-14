import logging

import django.contrib.auth
from django.core.management import BaseCommand
from cl8.users.importers import CATAirtableImporter
from pathlib import Path

logger = logging.getLogger(__name__)
console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# logger.addHandler(console)
# logger.setLevel(logging.DEBUG)


class Command(BaseCommand):
    help = "Import user profiles into this constellation "

    def handle(self, *args, **kwargs):
        importer = CATAirtableImporter()
        csv_path = Path() / "cat-directory.csv"

        importer.load_csv_from_path(csv_path)
        first_row = importer.rows[0]

        logger.debug(f"importing: {first_row}")
        users = importer.create_users(importer.rows)
        logger.debug(f"imported: {users}")
