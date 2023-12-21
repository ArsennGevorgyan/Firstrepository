from django.db.models import Q


def get_similar_products(product, inst_):
    return product.objects.filter(
        (Q(price__lte=inst_.price + 30) & Q(price__gte=inst_.price - 30))
        | (
                Q(calories__lte=inst_.calories + 30)
                & Q(calories__gte=inst_.calories - 30)
        ),
        ~Q(id=inst_.id),
    )
