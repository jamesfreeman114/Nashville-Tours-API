
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from toursapi.views import (
    register_user,
    login_user,
    get_current_user,
    TripView, VehicleView, TripVehicleView, ReservationView
    )


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'trips', TripView, 'trip')
router.register(r'vehicles', VehicleView, 'vehicle')
router.register(r'tripvehicles', TripVehicleView, 'tripvehicle')
router.register(r'reservations', ReservationView, 'reservation')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('current_user', get_current_user),
]




