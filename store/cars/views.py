from lib2to3.fixes.fix_input import context

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from cars.models import CarCategory, Car, Basket
from pyexpat.errors import messages


def index(request):
    return render(request,"cars/index.html")

def cars(request):
    # Этот context нужен для карточек товара и отображения всех категорий, которые находятся в базе данных
    context = {
        'cars': Car.objects.all(),
        'categories': CarCategory.objects.all(),
    }

    return render(request, "cars/cars.html", context)

def basket_add(request, car_id):
    car = Car.objects.get(id=car_id)
    baskets = Basket.objects.filter(user=request.user, car=car)

    if not baskets.exists():
        Basket.objects.create(user=request.user, car=car)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        basket = baskets.first()
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def basket_delete(request, basket_id):
    basket_remove = Basket.objects.get(id=basket_id)
    basket_remove.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def page_booking(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    context = {
        'car': car,
    }

    return render(request, "cars/page_booking.html", context)