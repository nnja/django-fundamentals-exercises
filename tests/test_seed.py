import io

import pytest
from django.core.management import call_command

from animals.models import AdoptionApplication, Animal

pytestmark = pytest.mark.django_db


def run_seed():
    out = io.StringIO()
    call_command("seed", stdout=out)
    return out.getvalue()


def test_seed_creates_three_animals():
    run_seed()
    animals = {animal.name: animal for animal in Animal.objects.all()}
    assert sorted(animals) == ["Peanut", "Rocket", "Smokey"]
    assert animals["Rocket"].species == Animal.Species.DOG
    assert animals["Rocket"].breed == "Beagle mix"
    assert animals["Peanut"].species == Animal.Species.CAT
    assert animals["Smokey"].species == Animal.Species.CAT
    assert animals["Smokey"].status == Animal.Status.PENDING
    available = Animal.objects.filter(status=Animal.Status.AVAILABLE)
    assert sorted(available.values_list("name", flat=True)) == ["Peanut", "Rocket"]


def test_seed_animals_have_their_ages():
    run_seed()
    labels = {animal.name: animal.age_label() for animal in Animal.objects.all()}
    assert labels == {"Rocket": "Adult", "Peanut": "Kitten", "Smokey": "Adult"}
    oldest_first = Animal.objects.order_by("birth_date").values_list("name", flat=True)
    assert list(oldest_first) == ["Smokey", "Rocket", "Peanut"]


def test_seed_creates_two_applications_for_peanut():
    run_seed()
    peanut = Animal.objects.get(name="Peanut")
    names = peanut.applications.values_list("applicant_name", flat=True)
    assert set(names) == {"Maria", "Aisha"}
    assert AdoptionApplication.objects.count() == 2


def test_seed_rows_are_valid():
    run_seed()
    rows = [*Animal.objects.all(), *AdoptionApplication.objects.all()]
    assert len(rows) == 5
    for row in rows:
        row.full_clean()


def test_seed_can_run_again():
    run_seed()
    run_seed()
    assert Animal.objects.count() == 3
    assert AdoptionApplication.objects.count() == 2
