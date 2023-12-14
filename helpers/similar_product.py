from django.db.models import Q


def sim_prod(product, inst):
    similar_products = product.objects.filter(
        (Q(price__lte=inst.price + 5) & Q(price__gte=inst.price - 5))
        | (
                Q(calories__lte=inst.calories + 5)
                & Q(calories__gte=inst.calories - 5)
        ),
        ~Q(id=inst.id),
    )
    return similar_products
