#!/bin/bash

rm db.sqlite3
rm -rf ./toursapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations toursapi
python3 manage.py migrate toursapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata trips
python3 manage.py loaddata vehicles
python3 manage.py loaddata trip_vehicles
python3 manage.py loaddata reservations
python3 manage.py loaddata reviews