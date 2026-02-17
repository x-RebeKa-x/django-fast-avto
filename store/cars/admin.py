from django.contrib import admin

from cars.models import Car, CarCategory, Basket

admin.site.register(Car)
admin.site.register(CarCategory)
admin.site.register(Basket)