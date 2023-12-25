import logging

from django.core.management import BaseCommand
from cl8.users.importers import CSVImporter

logger = logging.getLogger(__name__)
console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# logger.addHandler(console)
# logger.setLevel(logging.DEBUG)


class Command(BaseCommand):
    help = "Import user profiles into constallte "

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str)

    def handle(self, *args, **options):
        importer = CSVImporter()

        csv_path = options.get("csv_path")

        # import ipdb; ipdb.set_trace()

        importer.load_csv_from_path(csv_path)
        first_row = importer.rows[1]

        logger.debug(f"importing: {first_row}")
        users = importer.create_users(importer.rows)
        logger.debug(f"imported: {users}")
        # logger.debug(f"No of profiles to import: {len(importer.rows)}")
        # logger.debug(f"No of profiles to import: {len(importer.rows)}")
