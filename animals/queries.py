from .models import Animal


def all_animals():
    return Animal.objects.order_by("-intake_date", "name", "id")


def available_animals():
    return all_animals().filter(status=Animal.Status.AVAILABLE)


def listed_animals():
    return all_animals().exclude(status=Animal.Status.ADOPTED)
