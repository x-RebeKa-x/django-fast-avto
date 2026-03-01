from django.contrib import admin

from cars.models import Car, CarCategory, Basket

admin.site.register(CarCategory)
admin.site.register(Basket)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    # Отображает на главной панели имена, которые мы передадим
    list_display = ['name', 'price']
    # Создает фильтр по имени, которые мы передадим
    list_filter = ['category']
    # Создает поисковую строку
    search_fields = ['name']
    # Создаем свою последовательность ввода товара
    fields = ('name','image', ('price', 'quantity', 'category'), 'description', 'short_description')
    # Нельзя изменить, только для чтения
    readonly_fields = ('name', 'quantity')

class BasketAdminInline(admin.TabularInline):
    model = Basket
    fields = ('car', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp', )
    extra = 0