# RescueScout

A Django site for an animal rescue.

## Commands

- `uv sync` installs everything.
- `docker compose up -d --wait` starts Postgres and returns when it accepts connections. `docker compose down -v` deletes the database and everything in it.
- `uv run manage.py migrate` creates or updates the tables.
- `uv run manage.py seed` replaces the animals and adoption applications with three animals and two applications.
- `uv run manage.py runserver` serves the site at http://127.0.0.1:8000/.
- These checks must all pass before a change is done:

      uv run pytest
      uv run ruff check .
      uv run ruff format --check .
      uv run manage.py check
      uv run manage.py makemigrations --check --dry-run

- `uv run pytest` runs the tests on in-memory SQLite only, using `config/test_settings.py`, so they pass with the container stopped. That is on purpose.

## Rules

- This project uses Django 6.1. Do not use an API that was removed or deprecated before it.
- No type hints, in any file.
- A model change needs a migration: `uv run manage.py makemigrations`. Never edit a migration that has been applied.
- Imports between modules of the same app are relative: `from .models import Animal`. Imports in tests, in management commands, and across apps are absolute: `from animals.models import Animal`.
- Do not add dependencies, a frontend build step, or login. `psycopg` is the Postgres driver and is here because the project runs on Postgres.
- Connection values, `SECRET_KEY`, and `DEBUG` are written in `config/settings.py`. Do not add a `.env` file or read a setting from the environment.
- The `accounts` app and `tests/` are shared infrastructure. Change them only when asked.
