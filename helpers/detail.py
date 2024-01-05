from django.shortcuts import get_object_or_404, render
from django.views import View
from helpers.utils import get_similar_products


class DetailView(View):
    template_name = None
    model = None

    def get(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(self.model, pk=pk)
        similar_products = get_similar_products(self.model, instance)
        return render(
            request,
            self.template_name,
            {self.model.__name__.lower(): instance, "similar_products": similar_products},
        )
