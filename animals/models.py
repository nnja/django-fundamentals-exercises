from datetime import date, timedelta

from django.core.exceptions import ValidationError
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
        PENDING = "pending", "Adoption pending"
        ADOPTED = "adopted", "Adopted"

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=Species)
    breed = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField()
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="animals/", blank=True)
    status = models.CharField(max_length=10, choices=Status, default=Status.AVAILABLE)
    intake_date = models.DateField(default=date.today)

    class Meta:
        permissions = [
            (
                "manage_animal",
                "Can change an animal's status, and change adopted animals",
            ),
        ]

    def __str__(self):
        return self.name

    def age_label(self):
        """Puppy, Kitten, or Bunny under a year old; otherwise Adult."""
        if self.birth_date > date.today() - timedelta(days=365):
            # save() does not check choices, so the species may not be listed.
            return YOUNG_LABELS.get(self.species, "Young")
        return "Adult"


class AdoptionApplication(models.Model):
    """One visitor's request to adopt one animal.

    An employee approves or declines it in the admin. Approving one marks
    its animal pending.
    """

    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        APPROVED = "approved", "Approved"
        DECLINED = "declined", "Declined"

    animal = models.ForeignKey(
        Animal, on_delete=models.CASCADE, related_name="applications"
    )
    applicant_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="A US number, like 555-010-2000",
    )
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status, default=Status.SUBMITTED)
    # Set once, when the row is first saved.
    created_at = models.DateTimeField("submitted time", auto_now_add=True)

    def __str__(self):
        return f"{self.applicant_name} for {self.animal}"

    def save(self, **kwargs):
        super().save(**kwargs)
        # An approved application marks its animal pending.
        if (
            self.status == self.Status.APPROVED
            and self.animal.status == Animal.Status.AVAILABLE
        ):
            self.animal.status = Animal.Status.PENDING
            # Write the status column only, not the whole animal record.
            self.animal.save(update_fields=["status"])

    def clean(self):
        # Only an approval needs checking, and only once an animal is chosen.
        if self.status != self.Status.APPROVED or self.animal_id is None:
            return
        others = self.animal.applications.filter(status=self.Status.APPROVED)
        if others.exclude(pk=self.pk).exists():
            raise ValidationError(
                "Another application for this animal is already approved."
            )
