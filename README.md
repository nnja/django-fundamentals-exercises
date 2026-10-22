# RescueScout

An animal rescue site built with Django, one chapter at a time, in Django
Fundamentals. At this point the rescue's employees and volunteers can manage
animals, with their photos, in the admin, and employees review adoption
applications there, where only one application per animal can be approved.
Visitors browse the animals looking for a home a page at a time, search them
by name and species, open an animal's own page, and apply to adopt an
available animal.

## What is here

- `config/`: the project's settings and root URL patterns
- `templates/base.html` and `static/`: the site's layout, stylesheet, and fonts
- `compose.yaml`: Postgres 17 in Docker, started with `docker compose up -d --wait`
- `animals/`: the app, with its models, their migrations, the admin with its formset, the queries in `queries.py`, the pages' views and templates, the application form and the list page's search form, the phone number rule in `validators.py`, and the `seed` command
- `accounts/`: the custom user model, set before the first migration
- `seed_photos/`: the sample animals' photos, which the `seed` command copies, and their credits
- `manage.py`: runs Django's commands for this project
- `tests/`: tests for the adoption form
