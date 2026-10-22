from datetime import date, timedelta

from django.db import models

# What to call an animal under a year old, by species.
YOUNG_LABELS = {"dog": "Puppy", "cat": "Kitten", "rabbit": "Bunny"}


class Animal(models.Model):
    """One animal in the rescue's care, from intake until adoption.

    For a stray, the birth date is an estimate.
    """

    class Species(models.TextChoices):
        DOG = "dog", "Dog"
        CAT = "cat", "Cat"
        RABBIT = "rabbit", "Rabbit"

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        # TODO: Add PENDING, labeled "Adoption pending", and ADOPTED, labeled "Adopted".

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=Species)
    breed = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField()
    description = models.TextField(blank=True)
    # TODO: Add status, a CharField like species with the Status choices and a
    # default of available (Status.AVAILABLE).
    intake_date = models.DateField(default=date.today)

    def __str__(self):
        return self.name

    def age_label(self):
        """Puppy, Kitten, or Bunny under a year old; otherwise Adult."""
        if self.birth_date > date.today() - timedelta(days=365):
            # save() does not check choices, so the species may not be listed.
            return YOUNG_LABELS.get(self.species, "Young")
        return "Adult"
