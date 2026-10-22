# RescueScout

An animal rescue site built with Django, one chapter at a time, in Django
Fundamentals. At this point it has its two database tables, animals and the
adoption applications made for them, and a command that loads a few of each.

## What is here

- `config/`: the project's settings and root URL patterns
- `compose.yaml`: Postgres 17 in Docker, started with `docker compose up -d --wait`
- `animals/`: the app, with the `Animal` and `AdoptionApplication` models, their migrations, and the `seed` command
- `accounts/`: the custom user model, set before the first migration
- `manage.py`: runs Django's commands for this project
- `tests/`: tests for the seed command
