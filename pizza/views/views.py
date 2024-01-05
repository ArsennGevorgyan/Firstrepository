from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, DetailView, CreateView, ListView
from helpers.mixins import OwnProFileMixin
from pizza.forms import SearchForm, ProfileForm, UserRegistrationForm
from pizza.models import Pizza, Burger, Restaurant
from django.shortcuts import render
from django.contrib import messages


class PizzaListView(ListView):
    model = Pizza
    template_name = "pizza/all_pizza.html"
    context_object_name = "pizzas"
    paginate_by = 3
    ordering = ["-pk"]


class BurgerListView(ListView):
    model = Burger
    template_name = "pizza/burgers.html"
    context_object_name = "burgers"
    paginate_by = 3
    ordering = ["-pk"]


class RestaurantListView(ListView):
    model = Restaurant
    template_name = "pizza/restaurants.html"
    context_object_name = "restaurants"
    paginate_by = 4
    ordering = ["pk"]

    def get_queryset(self):
        return Restaurant.objects.all().prefetch_related("pizza", "burger").order_by("pk")


class AdvancedSearchView(View):
    template_name = 'pizza/search.html'

    def get(self, request, *args, **kwargs):
        form = SearchForm()
        result_product = []
        return render(request, self.template_name, {"form": form, "result_product": result_product})

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST)
        result_product = []
        if form.is_valid():
            name = form.cleaned_data.get("name")
            product_type = request.POST.get("product_type")
            rate_until = form.cleaned_data.get("rate_until")
            rate_from = form.cleaned_data.get("rate_from") or 0
            calories_until = request.POST.get("calories_until")

            result_q = Q()

            product_table = Burger if product_type == "burger" else Pizza

            if name:
                if product_type == "burger":
                    result_q &= Q(burger_name__icontains=name)
                else:
                    result_q &= Q(pizza_name__icontains=name)

            if rate_until:
                result_q &= Q(rate__lte=rate_until)

            result_q &= Q(rate__gte=rate_from)

            if calories_until:
                result_q &= Q(calories__lte=calories_until)

            result_product = product_table.objects.filter(result_q)

        return render(request, self.template_name, {"form": form, "result_product": result_product})


class AboutUsView(View):
    template_name = 'pizza/about_us.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class UserCreationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "user/registration.html"
    success_url = reverse_lazy("pizzas")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.profile.phone_number = form.cleaned_data["phone_number"]
        self.object.profile.country = form.cleaned_data["country"]
        self.object.profile.image = form.cleaned_data["image"]
        self.object.profile.user_type = form.cleaned_data["user_type"]
        self.object.profile.save()
        messages.success(self.request, "User Created Successfully")
        return response


class UserLoginView(LoginView):
    template_name = "user/login.html"


class UserLogoutView(LogoutView):
    pass


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "user/profile.html"


class UserUpdateView(OwnProFileMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "user/edit_profile.html"

    def get_initial(self):
        return {"phone_number": self.object.profile.phone_number,
                "country": self.object.profile.country,
                "image": self.object.profile.image}

    def get_success_url(self):
        messages.success(self.request, "User updated successfully!")
        return reverse("profile", kwargs={"pk": self.object.pk})
