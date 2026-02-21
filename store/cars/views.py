from lib2to3.fixes.fix_input import context

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from cars.models import CarCategory, Car, Basket
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime


def index(request):
    return render(request, "cars/index.html")


def cars(request, category_id=None, page=1):
    # Этот context нужен для карточек товара и отображения всех категорий, которые находятся в базе данных
    context = {
        'title': 'Car | Categories',
        'categories': CarCategory.objects.all(),
    }

    if category_id:
        filtered_cars = Car.objects.filter(category_id=category_id)
    else:
        filtered_cars = Car.objects.all()

    paginator = Paginator(filtered_cars, 6)
    cars_paginator = paginator.page(page)

    context['cars'] = cars_paginator

    return render(request, "cars/cars.html", context)


@login_required()
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

@login_required()
def page_booking(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        address = request.POST.get('address')
        date = request.POST.get('date')
        time = request.POST.get('time')
        date_end = request.POST.get('date_end')
        time_end = request.POST.get('time_end')
        payment_method = request.POST.get('payment_method')

        date_start_object = datetime.strptime(date, '%Y-%m-%d')
        date_end_object = datetime.strptime(date_end, '%Y-%m-%d')
        days = (date_end_object - date_start_object).days
        if days < 1:
            days = 1

        if days % 10 == 1 and days % 100 != 11:
            days_word = 'день'
        elif 2 <= days % 10 <= 4 and not (12 <= days % 100 <= 14):
            days_word = 'дня'
        else:
            days_word = 'дней'

        total_price = car.price * days

        booking_data = {
            'car_id': car.id,
            'car_name': car.name,
            'car_price': car.price,
            'address': address,
            'date': date,
            'time': time,
            'date_end': date_end,
            'time_end': time_end,
            'days': days,
            'days_word': days_word,
            'total_price': total_price,
            'payment_method': payment_method,
        }

        request.session['booking_data'] = booking_data

        return redirect('users:profile')

    context = {
        'car': car,
    }

    return render(request, "cars/page_booking.html", context)


def payment_page(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    booking_data = {
        'address': request.GET.get('address', ''),
        'date': request.GET.get('date', ''),
        'time': request.GET.get('time', ''),
        'date_end': request.GET.get('date_end', ''),
        'time_end': request.GET.get('time_end', ''),
    }

    session_data = request.session.get('booking_data', {})
    if session_data:
        booking_data.update(session_data)

    context = {
        'car': car,
        'booking': booking_data,
    }

    return render(request, "cars/payment_page.html", context)

