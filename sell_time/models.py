from django.db import models
from django.db import transaction
from decimal import Decimal

class TimePackage(models.Model):
    TYPE_CHOICES = (
        ('future', 'Towards Your Future'),
        ('past', 'For Your Past'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration_minutes = models.IntegerField()
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    use_type = models.CharField(max_length = 10, choices=TYPE_CHOICES, default = 'future')

    def __str__(self):
        return self.name
    
    @classmethod
    @transaction.atomic
    def seed_packages(cls):
        print(">>> Seeding 1k future and 1k past packages")
        future_existing = set(cls.objects.filter(use_type='future').values_list('duration_minutes', flat=True))
        past_existing = set(cls.objects.filter(use_type='past').values_list('duration_minutes', flat=True))
        future_to_create = []
        past_to_create = []
        for i in range(1, 1001):
            if i not in future_existing: 
                future_to_create.append(cls(
                    name = f"Future - {i} minutes",
                    description = "Package for future time usage", 
                    duration_minutes = i,
                    price = Decimal('15.00') * i,
                    use_type = 'future'
                ))     
            if i not in past_existing:
                past_to_create.append(cls(
                    name = f"Past - {i} minutes",
                    description = "Package for past time usage", 
                    duration_minutes = i,
                    price = Decimal('15.00') * i,
                    use_type = 'past'
                ))
            if i in future_existing and i in past_existing:
                print(f"Package with duration {i} already exists for both types.")

        cls.objects.bulk_create(future_to_create, ignore_conflicts=True)
        cls.objects.bulk_create(past_to_create, ignore_conflicts=True)
        print(f">>> Created {len(future_to_create)} new 'future' packages.")
        print(f">>>Created {len(past_to_create)} new 'past' packages.")
        return True  
