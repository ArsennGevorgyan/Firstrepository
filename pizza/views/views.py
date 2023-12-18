from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from pizza.forms import SearchForm
from pizza.models import Pizza, Burger, Restaurant


def pizza(request):
    pizzas = Pizza.objects.all().order_by("-pk")
    paginator = Paginator(pizzas, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "pizza/all_pizza.html", {"pizzas": page_obj})


def burger(request):
    burgers = Burger.objects.all().order_by("-pk")
    paginator = Paginator(burgers, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "pizza/burgers.html", {"burgers": page_obj})


def all_restaurant(request):
    restaurants = Restaurant.objects.all().prefetch_related("pizza", "burger").order_by("pk")
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
