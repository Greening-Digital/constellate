import logging

from django.core.management import BaseCommand
from cl8.users.importers import SlackImporter
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import users from slack into this constellation "

    def handle(self, *args, **kwargs):
        importer = SlackImporter()
        imported_users = importer.import_users()

        if imported_users:
            self.stdout.write(
                self.style.SUCCESS(
                    f"OK Successfully imported {len(imported_users)} from the "
                    f"slack channel: #{settings.SLACK_CHANNEL_NAME}"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"OK - No users to import from slack channel: #{settings.SLACK_CHANNEL_NAME}"
                )
            )

