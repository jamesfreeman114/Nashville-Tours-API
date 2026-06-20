from django.db import models
from .trip import Trip
from .vehicle import Vehicle


class TripVehicle(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)