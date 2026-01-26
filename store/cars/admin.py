from django.contrib import admin

from cars.models import Car, CarCategory

admin.site.register(Car)
admin.site.register(CarCategory)