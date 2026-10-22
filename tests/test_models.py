import datetime as dt

import pytest

from animals.models import Animal

pytestmark = pytest.mark.django_db


def test_animal_defaults_to_available_and_arrived_today():
    animal = Animal.objects.create(
        name="Biscuit", species=Animal.Species.DOG, birth_date=dt.date(2023, 5, 1)
    )
    assert animal.status == Animal.Status.AVAILABLE
    assert animal.intake_date == dt.date.today()


def test_species_and_status_have_labels(make_animal):
    animal = make_animal(species=Animal.Species.RABBIT, status=Animal.Status.PENDING)
    assert animal.get_species_display() == "Rabbit"
    assert animal.get_status_display() == "Adoption pending"


def test_adopted_is_a_status_with_a_label(make_animal):
    animal = make_animal(status=Animal.Status.ADOPTED)
    animal.full_clean()
    assert animal.get_status_display() == "Adopted"
