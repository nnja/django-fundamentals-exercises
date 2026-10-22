"""Fixtures for the tests. pytest-django supplies `admin_client` and
`django_user_model`."""

import datetime as dt

import pytest

from animals.models import AdoptionApplication, Animal


@pytest.fixture
def make_animal(db):
    """Create an available adult dog named Biscuit; override any field by keyword."""

    def factory(**overrides):
        values = {
            "name": "Biscuit",
            "species": Animal.Species.DOG,
            "breed": "Beagle mix",
            "birth_date": dt.date.today() - dt.timedelta(days=3 * 365),
            "description": "A gentle dog who likes long walks.",
            "status": Animal.Status.AVAILABLE,
        }
        values.update(overrides)
        return Animal.objects.create(**values)

    return factory


@pytest.fixture
def make_application(make_animal):
    """Create a submitted application from Maria for a new or given animal."""

    def factory(animal=None, **overrides):
        values = {
            "applicant_name": "Maria",
            "email": "maria@example.com",
            "phone": "555-010-2000",
            "message": "We have a fenced yard and no other pets.",
        }
        values.update(overrides)
        return AdoptionApplication.objects.create(
            animal=animal or make_animal(), **values
        )

    return factory
