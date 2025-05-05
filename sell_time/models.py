from django.db import models
from django.db import transaction

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
        print(">>> seeding loop started")
        for i in range(1, 1001):
            package, created = cls.objects.update_or_create(
                duration_minutes = i, 
                use_type = 'future', 
                defaults = {
                    'name': f"Future - {i} minutes",
                    'description': "Package for future time usage", 
                    'price': 15.00 * 1,
                }
            )        
            
        for i in range(1, 1001):
            package, created = cls.objects.update_or_create(
                duration_minutes = i, 
                use_type = 'past', 
                defaults = {
                    'name': f"Past - {i} minutes",
                    'description': "Package for past time usage", 
                    'price': 15.00 * 1,
                }
            )
        return True  
