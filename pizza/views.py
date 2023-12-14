from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from helpers.similar_product import sim_prod
from pizza.forms import SearchForm, PizzaForm, BurgerForm
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
    restaurants = Restaurant.objects.all().order_by("pk")
    paginator = Paginator(restaurants, 6)
    page_number = request.GET.get("page")
    restaurants = paginator.get_page(page_number)
    return render(request, "pizza/restaurants.html", {"restaurants": restaurants})


def advanced_search(request):
    form = SearchForm()
    result_product = []
    if name := request.GET.get("name"):
        form = SearchForm(request.GET)
        if request.GET.get("product_type") == "burger":
            product_table = Burger
            name_search = Q(burger_name__icontains=name)
        else:
            product_table = Pizza
            name_search = Q(pizza_name__icontains=name)
        if form.is_valid():
            filters = [name_search]
            rate_until = form.cleaned_data.get("rate_until")
            rate_from = form.cleaned_data.get("rate_from")
            calories_until = form.cleaned_data.get("calories_until")
            if rate_from is not "0":
                filters.append(Q(rate__gte=rate_from))
            if rate_until is not "0":
                filters.append(Q(rate__lte=rate_until))
            if calories_until is not None:
                filters.append(Q(calories__lte=calories_until))
            result_product = product_table.objects.filter(*filters)
    return render(request, "pizza/search.html", {"form": form, "result_product": result_product})


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
