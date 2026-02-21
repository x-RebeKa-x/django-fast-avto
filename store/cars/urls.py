from django.urls import path
from cars.views import cars, basket_add, basket_delete, page_booking, payment_page

app_name = 'cars'

urlpatterns = [
    path('', cars, name='index'),
    path('/<int:category_id>', cars, name='category'),
    path('page/<int:page>', cars, name='page'),
    path('basket-add/<int:car_id>', basket_add, name='basket_add'),
    path('basket-delete/<int:basket_id>', basket_delete, name='basket_delete'),
    path('booking/<int:car_id>', page_booking, name='page_booking'),
    path('payment/<int:car_id>', payment_page, name='payment_page'),
]

