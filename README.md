# RescueScout

An animal rescue site built with Django, one chapter at a time, in Django
Fundamentals. At this point it is a Django project on Postgres with a custom
user model and its first model, `Animal`.

## What is here

- `config/`: the project's settings and root URL patterns
- `compose.yaml`: Postgres 17 in Docker, started with `docker compose up -d --wait`
- `animals/`: the app, with the `Animal` model
- `accounts/`: the custom user model, set before the first migration
- `manage.py`: runs Django's commands for this project
- `tests/`: tests for the `Animal` model's status
