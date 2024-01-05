from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView

from helpers.detail import DetailView
from pizza.forms import PizzaForm, BurgerForm, RestaurantForm
from pizza.models import Burger, Restaurant, Pizza
from django.forms import inlineformset_factory


class PizzaDetailView(DetailView):
    template_name = "details/pizza_detail.html"
    model = Pizza


class BurgerDetailView(DetailView):
    template_name = "details/burger_detail.html"
    model = Burger


class RestaurantDetailView(View):
    template_name = "pizza/restaurant_detail.html"

    def get(self, request, pk, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        items = restaurant.pizza.all()
        burgers = request.GET.get("burgers")
        if burgers == "True":
            items = restaurant.burger.all()

        return render(
            request,
            self.template_name,
            {"restaurant": restaurant, "items": items},
        )


class AddRestaurantView(View):
    template_name = "details/add_restaurant.html"
    PizzaFormSet = inlineformset_factory(Restaurant, Pizza, form=PizzaForm, extra=2, can_delete=False)
    BurgerFormSet = inlineformset_factory(Restaurant, Burger, form=BurgerForm, extra=2, can_delete=False)

    def get(self, request, *args, **kwargs):
        restaurant_form = RestaurantForm()
        pizza_formset = self.PizzaFormSet(instance=Restaurant(), prefix='pizzas')
        burger_formset = self.BurgerFormSet(instance=Restaurant(), prefix='burgers')
        return render(
            request,
            self.template_name,
            {"restaurant_form": restaurant_form, "pizza_formset": pizza_formset, "burger_formset": burger_formset},
        )

    def post(self, request, *args, **kwargs):
        restaurant_form = RestaurantForm(request.POST, request.FILES)
        pizza_formset = self.PizzaFormSet(request.POST, request.FILES, instance=Restaurant(), prefix='pizzas')
        burger_formset = self.BurgerFormSet(request.POST, request.FILES, instance=Restaurant(), prefix='burgers')

        if all([restaurant_form.is_valid(), pizza_formset.is_valid(), burger_formset.is_valid()]):
            restaurant_instance = restaurant_form.save()
            pizza_formset.instance = restaurant_instance
            pizza_formset.save()
            burger_formset.instance = restaurant_instance
            burger_formset.save()
            messages.success(request, "Restaurant added successfully!")
            return redirect("restaurants")

        return render(
            request,
            self.template_name,
            {"restaurant_form": restaurant_form, "pizza_formset": pizza_formset, "burger_formset": burger_formset},
        )


class AddPizzaView(View):
    template_name = "details/add_pizza.html"

    def get(self, request, *args, **kwargs):
        form = PizzaForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = PizzaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Pizza added successfully!")
            return redirect("pizzas")

        return render(request, self.template_name, {"form": form})


class AddBurgerView(View):
    template_name = "details/add_burger.html"

    def get(self, request, *args, **kwargs):
        form = BurgerForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = BurgerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Burger added successfully!")
            return redirect("burgers")

        return render(request, self.template_name, {"form": form})


class EditPizzaView(UpdateView):
    model = Pizza
    form_class = PizzaForm
    template_name = 'details/edit_pizza.html'

    def form_valid(self, form):
        messages.success(self.request, f"{form.instance.pizza_name} Updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('pizzas')


class EditBurgerView(UpdateView):
    model = Burger
    form_class = BurgerForm
    template_name = 'details/edit_burger.html'

    def form_valid(self, form):
        messages.success(self.request, f"{form.instance.burger_name} Updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('burgers')


class DeletePizzaView(DeleteView):
    model = Pizza
    template_name = 'details/delete_pizza.html'
    success_url = reverse_lazy('pizzas')

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, "Pizza deleted Successfully")
        return super().delete(request, *args, **kwargs)


class DeleteBurgerView(DeleteView):
    model = Burger
    template_name = 'details/delete_burger.html'
    success_url = reverse_lazy('burgers')

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, "Burger deleted successfully!")
        return super().delete(request, *args, **kwargs)
