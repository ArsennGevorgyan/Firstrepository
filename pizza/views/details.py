from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib import messages

from helpers.utils import get_similar_products
from pizza.forms import PizzaForm, BurgerForm, RestaurantForm
from pizza.models import Pizza, Restaurant, Burger


def pizza_detail(request, pk: int):
    pizza_inst = get_object_or_404(Pizza, pk=pk)
    similar_products = get_similar_products(Pizza, pizza_inst)
    return render(
        request,
        "details/pizza_detail.html",
        {"pizza": pizza_inst, "similar_products": similar_products},
    )


def burger_detail(request, pk: int):
    burger_inst = get_object_or_404(Burger, pk=pk)
    similar_products = get_similar_products(Burger, burger_inst)
    return render(
        request,
        "details/burger_detail.html",
        {"burger": burger_inst, "similar_products": similar_products},
    )


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    items = restaurant.pizza.all()
    if burgers := request.GET.get("burgers"):
        if burgers == "True":
            items = restaurant.burger.all()

    return render(
        request,
        "pizza/restaurant_detail.html",
        {"restaurant": restaurant, "items": items},
    )


def add_restaurant(request):
    PizzaFormSet = inlineformset_factory(Restaurant, Pizza, form=PizzaForm, extra=2, can_delete=False)
    BurgerFormSet = inlineformset_factory(Restaurant, Burger, form=BurgerForm, extra=2, can_delete=False)

    if request.method == "POST":
        restaurant_form = RestaurantForm(request.POST, request.FILES)
        pizza_formset = PizzaFormSet(request.POST, request.FILES, instance=Restaurant(), prefix='pizzas')
        burger_formset = BurgerFormSet(request.POST, request.FILES, instance=Restaurant(), prefix='burgers')

        if all([restaurant_form.is_valid(), pizza_formset.is_valid(), burger_formset.is_valid()]):
            restaurant_instance = restaurant_form.save()
            pizza_formset.instance = restaurant_instance
            pizza_formset.save()
            burger_formset.instance = restaurant_instance
            burger_formset.save()
            messages.success(request, "Restaurant added successfully!")
            return redirect("restaurants")

    else:
        restaurant_form = RestaurantForm()
        pizza_formset = PizzaFormSet(instance=Restaurant(), prefix='pizzas')
        burger_formset = BurgerFormSet(instance=Restaurant(), prefix='burgers')

    return render(
        request,
        "details/add_restaurant.html",
        {"restaurant_form": restaurant_form, "pizza_formset": pizza_formset, "burger_formset": burger_formset},
    )


def add_pizza(request):
    form = PizzaForm()
    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Pizza added successfully!")
            return redirect("pizzas")
    return render(request, "details/add_pizza.html", {"form": form})


def add_burger(request):
    form = BurgerForm()
    if request.method == "POST":
        form = BurgerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Burger added successfully!")
            return redirect("burgers")
    return render(request, "details/add_burger.html", {"form": form})


def edit_restaurant(request, pk: int):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    form = RestaurantForm(instance=restaurant)
    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            restaurant_instance = form.save()
            messages.success(request, f"{restaurant_instance.name} Updated successfully!")
            return redirect(restaurant_instance)
    return render(request, "details/edit_restaurant.html", {"form": form})


def edit_pizza(request, pk: int):
    pizza = get_object_or_404(Pizza, pk=pk)
    form = PizzaForm(instance=pizza)
    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES, instance=pizza)
        if form.is_valid():
            pizza_instance = form.save()
            messages.success(request, f"{pizza_instance.name} Updated successfully!")
            return redirect(pizza_instance)
    return render(request, "details/edit_pizza.html", {"form": form})


def edit_burger(request, pk: int):
    burger = get_object_or_404(Burger, pk=pk)
    form = BurgerForm(instance=burger)
    if request.method == "POST":
        form = BurgerForm(request.POST, request.FILES, instance=burger)
        if form.is_valid():
            burger_instance = form.save()
            messages.success(request, f"{burger_instance.name} Updated successfully!")
            return redirect(burger_instance)
    return render(request, "details/edit_burger.html", {"form": form})


def delete_restaurant(request, pk: int):
    restaurant = get_object_or_404(Pizza, pk=pk)
    if request.method == "POST":
        restaurant.delete()
        messages.info(request, "Restaurant deleted Successfully")
        return redirect("restaurant")
    return render(request, "details/delete_restaurant.html", {"restaurant": restaurant})


def delete_pizza(request, pk: int):
    pizza = get_object_or_404(Pizza, pk=pk)
    if request.method == "POST":
        pizza.delete()
        messages.info(request, "pizza deleted Successfully")
        return redirect("pizzas")
    return render(request, "details/delete_pizza.html", {"pizza": pizza})


def delete_burger(request, pk: int):
    burger = get_object_or_404(Burger, pk=pk)
    if request.method == "POST":
        burger.delete()
        messages.info(request, "Burger deleted successfully!")
        return redirect("burgers")
    return render(request, "details/delete_burger.html", {"burger": burger})
