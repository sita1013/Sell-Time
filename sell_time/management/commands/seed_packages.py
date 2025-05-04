from django.core.management.base import BaseCommand
from sell_time.models import TimePackage  # adjust for your app

class Command(BaseCommand):
    help = 'Seeds the database with TimePackage data'

    def handle(self, *args, **kwargs):
        updated = TimePackage.seed_packages()
        if updated:
            self.stdout.write(self.style.SUCCESS("TimePackages seeded successfully."))
        else:
            self.stdout.write(self.style.WARNING("No changes were made."))
