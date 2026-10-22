import logging

from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView

from . import queries
from .models import AdoptionApplication, Animal

logger = logging.getLogger(__name__)


class AnimalListView(ListView):
    paginate_by = 12

    def get_queryset(self):
        return queries.listed_animals()


class AnimalDetailView(DetailView):
    model = Animal


class AdoptView(CreateView):
    model = AdoptionApplication
    template_name = "animals/adopt.html"

    def dispatch(self, request, *args, **kwargs):
        self.animal = get_object_or_404(
            queries.available_animals(), pk=kwargs["animal_id"]
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["animal"] = self.animal
        return context
