"""Fixtures for the tests."""

import datetime as dt

import pytest

from animals.models import Animal


@pytest.fixture
def make_animal(db):
    """Create an adult dog named Biscuit; override any field by keyword."""

    def factory(**overrides):
        values = {
            "name": "Biscuit",
            "species": Animal.Species.DOG,
            "breed": "Beagle mix",
            "birth_date": dt.date.today() - dt.timedelta(days=3 * 365),
            "description": "A gentle dog who likes long walks.",
        }
        values.update(overrides)
        return Animal.objects.create(**values)

    return factory
