from django.contrib import admin

from pizza.models import Pizza, Burger, Restaurant, Profile

admin.site.register(Pizza)
admin.site.register(Burger)
admin.site.register(Restaurant)
admin.site.register(Profile)
