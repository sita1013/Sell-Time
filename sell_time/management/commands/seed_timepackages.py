# management/commands/seed_timepackages.py

from django.core.management.base import BaseCommand
from sell_time.models import TimePackage  

class Command(BaseCommand):
    help = 'Seeds the database with TimePackage data'

    def handle(self, *args, **kwargs):
        seeded = TimePackage.seed_packages()

        if seeded:
            self.stdout.write(self.style.SUCCESS("Successfully seeded TimePackages."))
        else:
            self.stdout.write(self.style.WARNING("TimePackages already exist. Skipping."))
