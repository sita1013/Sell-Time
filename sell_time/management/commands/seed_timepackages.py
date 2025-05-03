from django.core.management.base import BaseCommand
from sell_time.models import TimePackage

class Command(BaseCommand):
    help = 'Seeds the database with TimePackage data'

    def handle(self, *args, **kwargs):
        if TimePackage.objects.exists():
            self.stdout.write(self.style.WARNING("TimePackages already exist. Skipping.")) 
            #stupidly embedded loops into my local django shell before realising this will cause issues in deployment
            return

        for i in range(1, 10001):
            TimePackage.objects.create(
                name=f"Future Use - {i} minutes",
                description="Package for future time usage",
                duration_minutes=i,
                price=50.00 * i, 
                use_type='future',
            )

        for i in range(1, 1001):
            TimePackage.objects.create(
                name=f"Past Use - {i} minutes",
                description="Package for past time usage",
                duration_minutes=i,
                price=50.00 * i,
                use_type='past',
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded TimePackages."))
