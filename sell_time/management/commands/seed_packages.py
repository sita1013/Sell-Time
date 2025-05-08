from django.core.management.base import BaseCommand
from sell_time.models import TimePackage, Purchase
from django.contrib.auth.models import User
from faker import Faker
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Seeds the database with TimePackage and Purchase data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        self.stdout.write(">>> Started seeding")
        try:
            updated = TimePackage.seed_packages()
            if updated:
                self.stdout.write(self.style.SUCCESS("TimePackages seeded successfully."))
            else:
                self.stdout.write(self.style.WARNING("No changes were made."))
        except Exception as e:
            self.stderr.write(f"Error while seeding: {e}")
        #for faker test users
        for i in range(10):
            username = fake.user_name()
            if not User.objects.filter(username = username).exists():
                User.objects.create_user(username = username, email = fake.email(), password = "testpass")
        users = list(User.objects.all())
        unassigned = TimePackage.objects.filter(creator__isnull = True)
        for pkg in unassigned[:30]:
            pkg.creator = random.choice(users)
            pkg.save()
        #fake purchases
        packages = list(TimePackage.objects.all())
        for i in range(40):
            user = random.choice(users)
            package = random.choice(packages)
            Purchase.objects.create(
                user = user, 
                email = user.email, 
                package = package, 
                quantity = random.randint(1, 2)
            )
        self.stdout.write(self.style.SUCCESS("Fake users, purchases, and sales created."))
        self.stdout.write(f"{len(users)} users total.")
        assigned_count = min(len(unassigned), 30)
        self.stdout.write(f"{assigned_count} packages assigned to users.")