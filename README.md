# RescueScout

An animal rescue site built with Django, one chapter at a time, in Django
Fundamentals. At this point it is the Django project `startproject` and
`startapp` generated, with two apps and a custom user model, and no models of
its own yet.

## What is here

- `config/`: the project's settings and root URL patterns
- `animals/`: the app the site's features go in
- `accounts/`: the custom user model, set before the first migration
- `compose.yaml`: Postgres 17 in Docker, started with `docker compose up -d --wait`
- `manage.py`: runs Django's commands for this project
- `pyproject.toml`: Django and the development tools, installed with `uv sync`
- `ruff.toml`: lint and format rules, with Ruff's Django rules turned on
- `.vscode/`: editor settings and recommended extensions
- `AGENTS.md`: instructions for AI coding agents
