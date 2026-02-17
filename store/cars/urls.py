from django.urls import path
from cars.views import cars, basket_add, basket_delete, page_booking

app_name = 'cars'

urlpatterns = [
    path('', cars, name='index'),
    path('basket-add/<int:car_id>', basket_add, name='basket_add'),
    path('basket-delete/<int:basket_id>', basket_delete, name='basket_delete'),
    path('booking/<int:car_id>', page_booking, name='page_booking'),
]

