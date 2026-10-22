from rest_framework import serializers

from .models import Animal


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = [
            # TODO: Add "url", which links each animal to its own endpoint.
            "id",
            "name",
            "species",
            "breed",
            "birth_date",
            "age_label",
            "description",
            "photo",
            "status",
            "intake_date",
        ]
