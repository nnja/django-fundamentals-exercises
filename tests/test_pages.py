import datetime as dt

import pytest
from django.core.files.base import ContentFile
from django.urls import reverse

from animals.models import Animal
from tests.conftest import png_bytes

pytestmark = pytest.mark.django_db


def test_detail_page_shows_the_animal(client, make_animal):
    animal = make_animal(name="Clover", breed="Tabby", description="Loves windowsills.")
    response = client.get(reverse("animals:detail", args=[animal.pk]))
    content = response.content.decode()
    assert response.status_code == 200
    for text in ["Clover", "Tabby", "Loves windowsills.", "Adult", "Available"]:
        assert text in content


def test_detail_page_404_for_unknown_animal(client):
    assert client.get(reverse("animals:detail", args=[999])).status_code == 404


def test_detail_page_shows_an_adopted_animal_with_its_status(client, make_animal):
    animal = make_animal(status=Animal.Status.ADOPTED)
    content = client.get(reverse("animals:detail", args=[animal.pk])).content.decode()
    assert "Adopted" in content


def test_detail_page_title_starts_with_the_name(client, make_animal):
    animal = make_animal(name="Clover")
    content = client.get(reverse("animals:detail", args=[animal.pk])).content.decode()
    assert "<title>Clover" in content


def test_detail_page_shows_the_photo(client, make_animal, media_root):
    animal = make_animal(name="Clover")
    animal.photo.save("clover.png", ContentFile(png_bytes()), save=True)
    content = client.get(reverse("animals:detail", args=[animal.pk])).content.decode()
    assert 'src="/media/animals/clover.png"' in content


def test_detail_page_shows_the_species_and_arrival_date(client, make_animal):
    animal = make_animal(species=Animal.Species.CAT, intake_date=dt.date(2026, 10, 12))
    content = client.get(reverse("animals:detail", args=[animal.pk])).content.decode()
    assert "Cat" in content
    # The date filter's "j F Y": the day without a leading zero, then the month's name.
    assert "12 October 2026" in content


def test_detail_page_leaves_out_an_empty_breed(client, make_animal):
    animal = make_animal(breed="")
    content = client.get(reverse("animals:detail", args=[animal.pk])).content.decode()
    assert "Breed" not in content


def test_detail_page_links_back_to_the_list(client, make_animal):
    animal = make_animal()
    content = client.get(reverse("animals:detail", args=[animal.pk])).content.decode()
    assert f'href="{reverse("animals:list")}">All animals' in content


def test_description_keeps_its_paragraphs(client, make_animal):
    animal = make_animal(description="Loves naps.\n\nAlso loves snacks.")
    content = client.get(reverse("animals:detail", args=[animal.pk])).content.decode()
    assert "<p>Loves naps.</p>" in content
    assert "<p>Also loves snacks.</p>" in content


def test_description_html_is_shown_as_text(client, make_animal):
    animal = make_animal(description="Not <b>bold</b>.")
    content = client.get(reverse("animals:detail", args=[animal.pk])).content.decode()
    assert "Not &lt;b&gt;bold&lt;/b&gt;." in content
    assert "<b>bold</b>" not in content
