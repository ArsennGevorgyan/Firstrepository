from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect

from helpers.similar_product import sim_prod
from pizza.forms import SearchForm, PizzaForm, BurgerForm, RestaurantForm
from pizza.models import Pizza, Burger, Restaurant


def pizza(request):
    pizzas = Pizza.objects.all()
    paginator = Paginator(pizzas, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "pizza/all_pizza.html", {"pizzas": page_obj})


def pizza_detail(request, pk: int):
    pizza_inst = get_object_or_404(Pizza, pk=pk)
    similar_products = sim_prod(Pizza, pizza_inst)
    return render(
        request,
        "details/pizza_detail.html",
        {"pizza": pizza_inst, "similar_products": similar_products},
    )


def burger(request):
    burgers = Burger.objects.all()
    paginator = Paginator(burgers, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "pizza/burgers.html", {"burgers": page_obj})


def burger_detail(request, pk: int):
    burger_inst = get_object_or_404(Burger, pk=pk)
    similar_products = sim_prod(Burger, burger_inst)
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


def all_restaurant(request):
    restaurants = Restaurant.objects.prefetch_related("pizza", "burger").order_by("pk")
    paginator = Paginator(restaurants, 6)
    page_number = request.GET.get("page")
    restaurants = paginator.get_page(page_number)
    return render(request, "pizza/restaurants.html", {"restaurants": restaurants})


def advanced_search(request):
    form = SearchForm()
    result_product = []
    if name := request.GET.get("name"):
        result_q = Q()
        form = SearchForm(request.GET)
        product_table = Pizza
        if form.is_valid():
            if request.GET.get("product_type") == "burger":
                product_table = Burger
                result_q &= Q(burger_name__icontains=name)
            else:
                result_q &= Q(pizza_name__icontains=name)
            if rate_until := form.cleaned_data.get("rate_until"):
                result_q &= Q(rate__lte=rate_until)
            result_q &= Q(rate__gte=form.cleaned_data["rate_from"] or 0)
            if calories_until := request.GET.get("calories_until"):
                result_q &= Q(calories__lte=calories_until)
            result_product = product_table.objects.filter(result_q)
    return render(request, "pizza/search.html", {"form": form,
                                                 "result_product": result_product})


def about_us(request):
    return render(request, "pizza/about_us.html")


def add_pizza(request):
    form = PizzaForm()
    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("pizzas")
    return render(request, "pizza/add_product.html", {"form": form})


def add_burger(request):
    form = BurgerForm()
    if request.method == "POST":
        form = BurgerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("burgers")
    return render(request, "pizza/add_product.html", {"form": form})


def add_restaurant(request):
    form = RestaurantForm()
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("restaurants")
    return render(request, "pizza/add_product.html", {"form": form})


def update_pizza(request, pk: int):
    pizza = get_object_or_404(Pizza, pk=pk)
    form = PizzaForm(instance=pizza)
    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES, instance=pizza)
        if form.is_valid():
            form.save()
            messages.info(request, "Pizza was updated successfully!")
            return redirect(pizza)
    return render(request, "pizza/update_pizza.html", {"form": form})


def update_burger(request, pk: int):
    burger = get_object_or_404(Burger, pk=pk)
    form = BurgerForm(instance=burger)
    if request.method == "POST":
        form = BurgerForm(request.POST, request.FILES, instance=burger)
        if form.is_valid():
            form.save()
            messages.info(request, "Burger was updated successfully!")
            return redirect(pizza)
    return render(request, "pizza/update_burger.html", {"form": form})


def delete_pizza(request, pk: int):
    pizza = get_object_or_404(Pizza, pk=pk)
    if request.method == "POST":
        pizza.delete()
        messages.info(request, "Pizza was deleted successfully!")
        return redirect("pizzas")
    return render(request, "pizza/delete_pizza.html", {"pizza": pizza})


def delete_burger(request, pk: int):
    burger = get_object_or_404(Burger, pk=pk)
    if request.method == "POST":
        burger.delete()
        messages.info(request, "Burger was deleted successfully!")
        return redirect("burgers")
    return render(request, "pizza/delete_burger.html", {"burger": burger})


def add_restaurant_with_products(request):
    pizza_form_set = inlineformset_factory(Restaurant, Pizza, form=PizzaForm, extra=2, can_delete=False)
    burger_form_set = inlineformset_factory(Restaurant, Burger, form=BurgerForm, extra=2, can_delete=False)
    if request.method == "POST":
        restaurant_form = RestaurantForm(request.POST, request.FILES)
        pizza_formset = pizza_form_set(request.POST, request.FILES, instance=restaurant_form.instance, prefix='pizzas')
        burger_formset = burger_form_set(request.POST, request.FILES, instance=restaurant_form.instance,
                                        prefix='burgers')
        if all([restaurant_form.is_valid(), pizza_formset.is_valid(), burger_formset.is_valid()]):
            restaurant_form.save()
            pizza_formset.save()
            burger_formset.save()
            return redirect("restaurants")
    else:
        restaurant_form = RestaurantForm()
        pizza_formset = pizza_form_set(instance=Restaurant(), prefix='pizzas')
        burger_formset = burger_form_set(instance=Restaurant(), prefix='burgers')
    return render(
        request,
        "pizza/add_restaurant_with_products.html",
        {"restaurant_form": restaurant_form, "pizza_formset": pizza_formset, "burger_formset": burger_formset},
    )
