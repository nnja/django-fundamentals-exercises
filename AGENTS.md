# RescueScout

A Django site for an animal rescue.

## Commands

- `uv sync` installs everything.
- These checks must all pass before a change is done:

      uv run ruff check .
      uv run ruff format --check .

## Rules

- This project uses Django 6.1. Do not use an API that was removed or deprecated before it.
- No type hints, in any file.
- Do not add dependencies, a frontend build step, or login.
