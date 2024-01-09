from django.urls import path
from .views import pizza, burger, about_us, all_restaurant, \
    restaurant_detail, pizza_detail, burger_detail, \
    advanced_search, add_pizza, add_burger, update_burger, update_pizza, delete_pizza, delete_burger,  \
    add_restaurant_with_products

urlpatterns = [
    path("", pizza, name="pizzas"),
    path("pizza/detail/<int:pk>/", pizza_detail, name="pizza_details"),
    path("burger/detail/<int:pk>/", burger_detail, name="burger_detail"),
    path("burgers/", burger, name="burgers"),
    path("about-us/", about_us, name="about_us"),
    path("restaurants/", all_restaurant, name="restaurants"),
    path("restaurant/<int:pk>/", restaurant_detail, name="res_detail"),
    path("search/", advanced_search, name="search"),
    path("add-pizza/", add_pizza, name="add_pizza"),
    path("add-burger/", add_burger, name="add_burger"),
    path("update-pizza/<int:pk>/", update_pizza, name="update_pizza"),
    path("update-burger/<int:pk>/", update_burger, name="update_burger"),
    path("delete-pizza/<int:pk>/", delete_pizza, name="delete_pizza"),
    path("delete-burger/<int:pk>/", delete_burger, name="delete_burger"),
    path("add_restaurant_with_products/", add_restaurant_with_products, name="add_restaurant_with_products"),
]
