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
    use_type = models.CharField(max_length = 10, choices = TYPE_CHOICES, default = 'future')

    def __str__(self):
        return self.name
