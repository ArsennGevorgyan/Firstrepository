from django import forms

from helpers.choices import RATE_CHOICES, PRODUCT_TYPE_CHOICES
from pizza.models import Pizza, Burger


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["calories_until"].widget.attrs.update(
            {"class": "form-control search-slt"}
        )
        self.fields["name"].widget.attrs.update(
            {"class": "form-control search-slt", "placeholder": "Name"}
        )

    name = forms.CharField(max_length=100, label="Product Name", required=True)
    rate_from = forms.ChoiceField(
        choices=RATE_CHOICES,
        widget=forms.Select(
                            attrs={"class": "form-control search-slt"}
                            ), label="Rate From", required=False, initial=None
    )
    rate_until = forms.ChoiceField(
        choices=RATE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control search-slt"},
                            ), label="Rate Until", required=False, initial=None
    )
    calories_until = forms.FloatField(max_value=1000, min_value=1,
                                      label="Calories Until",
                                      required=False)
    product_type = forms.ChoiceField(choices=PRODUCT_TYPE_CHOICES,
                                     widget=forms.Select(attrs={"class": "form-control search-slt"}
                                                         ), required=False)


class PizzaForm(forms.ModelForm):

    class Meta:
        model = Pizza
        fields = ("name", "description",
                  "rate", "prepare_time", "calories",
                  "price", "image", "restaurant")


class BurgerForm(forms.ModelForm):

    class Meta:
        model = Burger
        fields = ("name", "description",
                  "rate", "prepare_time", "calories",
                  "price", "image", "restaurant")
