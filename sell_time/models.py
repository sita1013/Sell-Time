# models.py

from django.db import models

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
    def seed_packages(cls):
        if cls.objects.exists():
            return False 

        future_packages = [
            cls(
                name = f"Future - {i} minutes",
                description = "Package for future time usage",
                duration_minutes = i,
                price = 15.00 * i,
                use_type = 'future',
            )
            for i in range(1, 10001)
        ]

        past_packages = [
            cls(
                name = f"Past - {i} minutes",
                description = "Package for past time usage",
                duration_minutes = i,
                price = 15.00 * i,
                use_type = 'past',
            )
            for i in range(1, 1001)
        ]

        cls.objects.bulk_create(future_packages + past_packages)
        return True  
