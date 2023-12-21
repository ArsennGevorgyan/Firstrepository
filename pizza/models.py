from django.db import models
from django.urls import reverse

from helpers.media_upload import upload_pizza_image, upload_burger_image, upload_restaurant
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from helpers.media_upload import upload_user_images
from django.dispatch import receiver
from django.db.models.signals import post_save


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_user_images, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    phone_field = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def profile_post_save(instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
