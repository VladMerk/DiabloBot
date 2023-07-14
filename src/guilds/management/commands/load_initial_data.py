import logging
from typing import Any, Optional
from django.core.management.base import BaseCommand
from django.core.management import call_command

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Loads initial data about `TerrorZone` into database"

    def handle(self, *args: Any, **options: Any) -> str | None:
        from guilds.models import TerrorZones

        if not TerrorZones.objects.exists():
            call_command('loaddata', 'terror_zone.json')
        else:
            logger.info("Data already exists in database. Skipping data load...")
