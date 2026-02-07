from django.db import models

# КАРТОЧКА КАТЕГОРИИ АВТОМОБИЛЯ
class CarCategory(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# КАРТОЧКА АВТОМОБИЛЯ
class Car(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cars/')
    description = models.TextField()
    short_description = models.TextField(max_length=64, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    # нельзя удалить категорию пока не удалить все товары связанные с ним
    category = models.ForeignKey(CarCategory, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} | {self.category.name}'
