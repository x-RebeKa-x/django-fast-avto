from django.contrib import admin
from users.models import User
from cars.admin import BasketAdminInline

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (BasketAdminInline,)
