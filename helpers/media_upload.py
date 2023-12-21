def upload_pizza_image(instance, filename):
    return f"pizzas/{instance.name}/{filename}"


def upload_burger_image(instance, filename):
    return f"burgers/{instance.name}/{filename}"


def upload_restaurant(instance, filename):
    return f"restaurant/{instance.name}/{filename}"


def upload_user_images(instance, filename):
    return f"users/{instance.user.username}/{filename}"
