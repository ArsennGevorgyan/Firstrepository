from django.db import models
from django.urls import reverse

from helpers.media_upload import upload_pizza_image, upload_burger_image, upload_restaurant


class Restaurant(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_restaurant)
    creation_date = models.DateField()

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    rate = models.FloatField(default=0)
    prepare_time = models.FloatField(null=True, blank=True)
    calories = models.FloatField(blank=True)
    price = models.FloatField()
    image = models.ImageField(upload_to=upload_pizza_image, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
                                   related_name="pizza")

    def get_absolute_url(self):
        return reverse("pizza_details", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class Burger(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    rate = models.FloatField(default=0)
    prepare_time = models.FloatField(null=True, blank=True)
    calories = models.FloatField(blank=True)
    price = models.FloatField()
    image = models.ImageField(upload_to=upload_burger_image, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
                                   related_name="burger")

    def get_absolute_url(self):
        return reverse("burger_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name
