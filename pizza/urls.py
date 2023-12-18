from django.urls import path
from pizza.views import pizza, burger, about_us, \
    all_restaurant, restaurant_detail, pizza_detail, burger_detail, \
    advanced_search, add_pizza, add_burger
from pizza.views.details import edit_pizza, edit_burger, delete_burger, delete_pizza

urlpatterns = [
    path("", pizza, name="pizzas"),
    path("pizza/detail/<int:pk>/", pizza_detail, name="pizza_details"),
    path("add-pizza/", add_pizza, name="add_pizza"),
    path("update-pizza/<int:pk>/", edit_pizza, name="edit_pizza"),
    path("delete-pizza/<int:pk>/", delete_pizza, name="delete_pizza"),
    path("add-burger/", add_burger, name="add_burger"),
    path("burger/detail/<int:pk>/", burger_detail, name="burger_detail"),
    path("update-burger/<int:pk>/", edit_burger, name="edit_burger"),
    path("delete-burger/<int:pk>/", delete_burger, name="delete_burger"),
    path("burgers/", burger, name="burgers"),
    path("about-us/", about_us, name="about_us"),
    path("restaurants/", all_restaurant, name="restaurants"),
    path("restaurant/<int:pk>/", restaurant_detail, name="restaurant_detail"),
    path("search/", advanced_search, name="search"),
]
