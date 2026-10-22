"""Fixtures for the tests. pytest-django supplies `client` and `settings`."""

import datetime as dt
import io

import pytest
from PIL import Image

from animals.models import Animal


def png_bytes(color="#f2a93b"):
    """A 4x4 PNG, enough for an ImageField to accept."""
    buffer = io.BytesIO()
    Image.new("RGB", (4, 4), color).save(buffer, format="PNG")
    return buffer.getvalue()


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
def media_root(settings, tmp_path):
    """Point uploads at a temporary directory so tests never write into media/."""
    settings.MEDIA_ROOT = tmp_path / "media"
    return settings.MEDIA_ROOT
