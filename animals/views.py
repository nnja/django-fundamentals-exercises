from django.views.generic import DetailView, ListView

from . import queries
from .models import Animal


class AnimalListView(ListView):
    paginate_by = 12

    def get_queryset(self):
        return queries.listed_animals()


class AnimalDetailView(DetailView):
    # TODO: Set `model`, so DetailView knows which table to look the animal up in.
    pass
