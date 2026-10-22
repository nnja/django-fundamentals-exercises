from datetime import date, timedelta

from django.core.management.base import BaseCommand

from animals.models import AdoptionApplication, Animal


class Command(BaseCommand):
    help = "Replace every animal with three animals and two adoption applications."

    def handle(self, *args, **options):
        # Deleting the animals also deletes their applications, so the command
        # can run again.
        Animal.objects.all().delete()

        peanut = Animal.objects.create(
            name="Peanut",
            species=Animal.Species.CAT,
            birth_date=date.today() - timedelta(days=60),
        )
        # TODO: Create Rocket, a dog born 3 years ago (3 * 365 days),
        # with a breed of "Beagle mix".
        # TODO: Create Smokey, a cat born 4 years ago (4 * 365 days),
        # with a status of pending.

        AdoptionApplication.objects.create(
            animal=peanut, applicant_name="Maria", email="maria@example.com"
        )
        # TODO: Create Aisha's application for Peanut, with an email of
        # aisha@example.com.

        self.stdout.write("Created 3 animals and 2 adoption applications.")
