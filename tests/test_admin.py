import pytest
from django.contrib.auth.models import Group, Permission
from django.test import Client
from django.urls import reverse

from animals.management.commands.seed import GROUPS
from animals.models import Animal

pytestmark = pytest.mark.django_db


def test_application_list_has_a_status_filter(admin_client, make_application):
    make_application()
    url = reverse("admin:animals_adoptionapplication_changelist")
    assert "By status" in admin_client.get(url).content.decode()


def test_application_search_matches_animal_name(
    admin_client, make_animal, make_application
):
    make_application(animal=make_animal(name="Clover"), applicant_name="Sam")
    make_application(applicant_name="Maria")
    url = reverse("admin:animals_adoptionapplication_changelist")
    content = admin_client.get(url, {"q": "clover"}).content.decode()
    assert "Sam" in content
    assert "Maria" not in content


def animal_form_data(animal, rows):
    """What the animal page posts: its own fields, then one inline row per
    (application id, status) pair. An id of None is a row added on the page."""
    data = {
        "name": animal.name,
        "species": animal.species,
        "breed": animal.breed,
        "birth_date": animal.birth_date.isoformat(),
        "description": animal.description,
        "status": animal.status,
        "intake_date": animal.intake_date.isoformat(),
        "applications-TOTAL_FORMS": str(len(rows)),
        "applications-INITIAL_FORMS": str(sum(1 for pk, _ in rows if pk)),
        "applications-MIN_NUM_FORMS": "0",
        "applications-MAX_NUM_FORMS": "1000",
    }
    for index, (pk, status) in enumerate(rows):
        data[f"applications-{index}-id"] = pk or ""
        data[f"applications-{index}-animal"] = animal.pk
        data[f"applications-{index}-status"] = status
    return data


def group_client(django_user_model, group_name):
    """A client logged in as an account in one of the seed's groups."""
    group = Group.objects.create(name=group_name)
    group.permissions.set(
        Permission.objects.filter(
            content_type__app_label="animals", codename__in=GROUPS[group_name]
        )
    )
    user = django_user_model.objects.create_user(group_name.lower(), is_staff=True)
    user.groups.add(group)
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def volunteer_client(django_user_model):
    return group_client(django_user_model, "Volunteers")


@pytest.fixture
def employee_client(django_user_model):
    return group_client(django_user_model, "Employees")


def test_a_volunteer_changes_an_animal_but_not_its_status(
    volunteer_client, make_animal
):
    animal = make_animal()
    url = reverse("admin:animals_animal_change", args=[animal.pk])
    content = volunteer_client.get(url).content.decode()
    assert 'name="name"' in content
    assert 'name="status"' not in content
    data = animal_form_data(animal, [])
    data |= {"breed": "Basset hound", "status": "adopted"}
    assert volunteer_client.post(url, data).status_code == 302
    animal.refresh_from_db()
    assert animal.breed == "Basset hound"
    assert animal.status == Animal.Status.AVAILABLE


def test_an_adopted_animal_is_read_only_for_a_volunteer(volunteer_client, make_animal):
    animal = make_animal(status=Animal.Status.ADOPTED)
    url = reverse("admin:animals_animal_change", args=[animal.pk])
    response = volunteer_client.get(url)
    # The view permission still shows the page, with every field as text.
    assert response.status_code == 200
    assert 'name="name"' not in response.content.decode()
    data = animal_form_data(animal, []) | {"breed": "Basset hound"}
    assert volunteer_client.post(url, data).status_code == 403
    animal.refresh_from_db()
    assert animal.breed == "Beagle mix"


def test_an_employee_changes_an_adopted_animal(employee_client, make_animal):
    animal = make_animal(status=Animal.Status.ADOPTED)
    url = reverse("admin:animals_animal_change", args=[animal.pk])
    data = animal_form_data(animal, []) | {"breed": "Basset hound"}
    assert employee_client.post(url, data).status_code == 302
    animal.refresh_from_db()
    assert animal.breed == "Basset hound"
