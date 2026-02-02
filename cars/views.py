from lib2to3.fixes.fix_input import context
from django.shortcuts import render

from cars.models import Car
from cars.models import CarCategory

def index(request):
    return render(request,"cars/index.html")

def cars(request):
    # Этот context нужен для карточек товара и отображения всех категорий, которые находятся в базе данных
    context = {
        'cars': Car.objects.all(),
        'categories': CarCategory.objects.all(),
    }

    return render(request, "cars/cars.html", context)

