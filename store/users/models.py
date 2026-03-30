from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    phone_number = PhoneNumberField(blank=True, null=True, help_text="Введите номер телефона", region='RU')

    def __str__(self):
        return self.username
