from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Vehicle(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])