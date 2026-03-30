from lib2to3.fixes.fix_input import context

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from cars.models import CarCategory, Car, Basket
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import datetime


def index(request, category_id=None, page=1):
    context = {
        'title': 'Car | Categories',
        'categories': CarCategory.objects.all(),
    }

    if category_id:
        filtered_cars = Car.objects.filter(category_id=category_id)
    else:
        filtered_cars = Car.objects.all()

    filtered_cars = filtered_cars.order_by('?')

    paginator = Paginator(filtered_cars, 3)
    cars_paginator = paginator.page(page)

    context['cars'] = cars_paginator

    return render(request, "cars/index.html", context)


def cars(request, category_id=None, page=1):
    # Этот context нужен для карточек товара и отображения всех категорий, которые находятся в базе данных
    price_range = request.GET.get('price')

    context = {
        'title': 'Car | Categories',
        'categories': CarCategory.objects.all(),
        'current_category': category_id,
        'current_price': price_range,
        'page': page,
    }

    if category_id:
        filtered_cars = Car.objects.filter(category_id=category_id)
    else:
        filtered_cars = Car.objects.all()

    if price_range:
        if price_range == '1000-2000':
            filtered_cars = filtered_cars.filter(price__gte=1000, price__lte=2000)
        elif price_range == '2000-3000':
            filtered_cars = filtered_cars.filter(price__gte=2000, price__lte=3000)
        elif price_range == '3000-5000':
            filtered_cars = filtered_cars.filter(price__gte=3000, price__lte=5000)
        elif price_range == '5000':
            filtered_cars = filtered_cars.filter(price__gte=5000)

    paginator = Paginator(filtered_cars, 9)

    try:
        cars_paginator = paginator.page(page)
    except PageNotAnInteger:
        cars_paginator = paginator.page(1)
    except EmptyPage:
        cars_paginator = paginator.page(paginator.num_pages)


    context['cars'] = cars_paginator

    return render(request, "cars/cars.html", context)


@login_required()
def basket_add(request, car_id):
    car = Car.objects.get(id=car_id)

    if Basket.objects.filter(user=request.user, status='active').exists():
        messages.error(request, 'У вас уже есть забронированная машина')
        return redirect('users:profile')

    if Basket.objects.filter(user=request.user, status='pending').exists():
        messages.error(request, 'У вас уже есть забронированная машина')
        return redirect('users:profile')

    card_number = request.POST.get('card_number')

    if card_number:
        status = 'active'
    else:
        status = 'pending'

    basket, created = Basket.objects.get_or_create(
        user=request.user,
        car=car,
        defaults={'status': status}
    )

    if not created:
        basket.status = status
        basket.save()
        return redirect('users:profile')
    return redirect('users:profile')


def basket_delete(request, basket_id):
    basket_remove = Basket.objects.get(id=basket_id)
    basket_remove.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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

        request.session['booking_data'] = {
            'car_id': car.id,
            'car_name': car.name,
            'car_price': str(car.price),
            'address': address,
            'date': date,
            'time': time,
            'date_end': date_end,
            'time_end': time_end,
            'days': days,
            'days_word': days_word,
            'total_price': str(total_price),
            'payment_method': payment_method,
        }

        return redirect('users:profile', car_id=car_id.id)

    context = {
        'car': car,
        'now': datetime.now(),
    }

    return render(request, "cars/page_booking.html", context)


def payment_page(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    session_data = request.session.get('booking_data', {})

    if not isinstance(session_data, str):
        session_data = {}

    booking_data = {
        'address': request.GET.get('address', ''),
        'date': request.GET.get('date', ''),
        'time': request.GET.get('time', ''),
        'date_end': request.GET.get('date_end', ''),
        'time_end': request.GET.get('time_end', ''),
    }

    if session_data and isinstance(session_data, dict):
        booking_data.update(session_data)

    if not session_data and request.method == 'POST':
        address = request.POST.get('address')
        date = request.POST.get('date')
        time = request.POST.get('time')
        date_end = request.POST.get('date_end')
        time_end = request.POST.get('time_end')

        if all([address, date, time, date_end, time_end]):
            date_start_object = datetime.strptime(date, '%Y-%m-%d').date()
            date_end_object = datetime.strptime(date_end, '%Y-%m-%d').date()
            time_start_object = datetime.strptime(time, '%H:%M').time()
            time_end_object = datetime.strptime(time_end, '%H:%M').time()

            if date_start_object == date_end_object and time_end_object < time_start_object:
                time_error = 'Время возврата не может быть раньше времени получения в один и тот же день'

                context = {
                    'car': car,
                    'time_error': time_error,
                    'now': datetime.now(),
                }
                return render(request, "cars/page_booking.html", context)

            if date_start_object > date_end_object:
                date_error = "Дата возврата не может быть раньше получения"

                context = {
                    'car': car,
                    'date_error': date_error,
                    'now': datetime.now(),
                }

                return render(request, 'cars/page_booking.html', context)


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
                'car_price': str(car.price),
                'address': address,
                'date': date,
                'time': time,
                'date_end': date_end,
                'time_end': time_end,
                'days': days,
                'days_word': days_word,
                'total_price': str(total_price),
            }

            request.session['booking_data'] = booking_data

    context = {
        'car': car,
        'booking': booking_data,
    }

    return render(request, "cars/payment_page.html", context)


def cheque(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    session_data = request.session.get('booking_data', {})

    if session_data and isinstance(session_data, dict):
        booking_data = session_data
    else:
        booking_data = {}

    context = {
        'car': car,
        'booking': booking_data
    }

    return render(request, "cars/cheque.html", context)


def custom_404(request, exception):
    return render(request, '404.html', status=404)
