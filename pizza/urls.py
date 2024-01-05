from django.urls import path
from pizza.views import (PizzaListView, BurgerListView, RestaurantListView,
                         PizzaDetailView, BurgerDetailView, RestaurantDetailView,
                         AddRestaurantView, AddPizzaView, AddBurgerView,
                         EditPizzaView, EditBurgerView, DeletePizzaView, DeleteBurgerView,
                         UserCreationView, UserLoginView, UserLogoutView, UserProfileView, UserUpdateView,
                         AdvancedSearchView, AboutUsView)

urlpatterns = [
    path("", PizzaListView.as_view(), name="pizzas"),
    path("burgers/", BurgerListView.as_view(), name="burgers"),
    path("restaurants/", RestaurantListView.as_view(), name="restaurants"),

    path("search/", AdvancedSearchView.as_view(), name="search"),
    path("about-us/", AboutUsView.as_view(), name="about_us"),

    path("pizza/detail/<int:pk>/", PizzaDetailView.as_view(), name="pizza_details"),
    path("burger/detail/<int:pk>/", BurgerDetailView.as_view(), name="burger_detail"),
    path("restaurant/<int:pk>/", RestaurantDetailView.as_view(), name="restaurant_detail"),

    path("add-pizza/", AddPizzaView.as_view(), name="add_pizza"),
    path("add-burger/", AddBurgerView.as_view(), name="add_burger"),
    path("create-restaurant/", AddRestaurantView.as_view(), name="add_restaurant"),

    path("update-pizza/<int:pk>/", EditPizzaView.as_view(), name="edit_pizza"),
    path("update-burger/<int:pk>/", EditBurgerView.as_view(), name="edit_burger"),
    path("delete-pizza/<int:pk>/", DeletePizzaView.as_view(), name="delete_pizza"),
    path("delete-burger/<int:pk>/", DeleteBurgerView.as_view(), name="delete_burger"),

    path("registration/", UserCreationView.as_view(), name="registration"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", UserProfileView.as_view(), name="profile"),
    path("edit-profile/<int:pk>/", UserUpdateView.as_view(), name="edit_profile"),
]
