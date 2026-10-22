import logging

import pytest
from django.contrib.messages import get_messages
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from animals.models import AdoptionApplication

pytestmark = pytest.mark.django_db

VALID_FORM = {
    "applicant_name": "Maria",
    "email": "maria@example.com",
    "phone": "555-010-2000",
    "message": "We have a fenced yard.",
}


def test_valid_post_creates_application_and_redirects(client, make_animal):
    animal = make_animal()
    response = client.post(reverse("animals:adopt", args=[animal.pk]), VALID_FORM)
    assertRedirects(response, reverse("animals:detail", args=[animal.pk]))
    application = AdoptionApplication.objects.get()
    assert application.animal == animal
    assert application.applicant_name == "Maria"
    assert application.status == AdoptionApplication.Status.SUBMITTED


def test_valid_post_logs_the_ids_and_nothing_about_the_applicant(
    client, make_animal, caplog
):
    # A second animal, so the two ids in the line are different numbers.
    make_animal(name="Maple")
    animal = make_animal(name="Clover")
    with caplog.at_level(logging.INFO, logger="animals.views"):
        client.post(reverse("animals:adopt", args=[animal.pk]), VALID_FORM)
    application = AdoptionApplication.objects.get()
    records = [record for record in caplog.records if record.name == "animals.views"]
    assert len(records) == 1
    assert records[0].levelno == logging.INFO
    # args are what the view passed for the %s placeholders in the message.
    assert records[0].args == (application.pk, animal.pk)
    line = records[0].getMessage()
    assert str(application.pk) in line
    assert str(animal.pk) in line
    assert VALID_FORM["applicant_name"] not in line
    assert VALID_FORM["email"] not in line


def test_valid_post_thanks_the_visitor_once(client, make_animal):
    animal = make_animal(name="Clover")
    url = reverse("animals:adopt", args=[animal.pk])
    # follow=True loads the page the redirect points to, as a browser does.
    response = client.post(url, VALID_FORM, follow=True)
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].level_tag == "success"
    thanks = str(messages[0])
    assert "Clover" in thanks
    assert thanks in response.content.decode()
    # The message is shown once: loading the page again does not repeat it.
    again = client.get(reverse("animals:detail", args=[animal.pk]))
    assert thanks not in again.content.decode()
