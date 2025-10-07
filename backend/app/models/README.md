# Backend Models Directory

Currently models are declared inline in `backend/app/database.py` using SQLAlchemy ORM classes.

Future actions:
- Move ORM class definitions from `database.py` into separate modules here (e.g. `aqi_reading.py`, `user.py`).
- Add Alembic migrations referencing these modules.
- Keep `__init__.py` to import and expose metadata for autogeneration.

Leaving this README prevents the directory from being empty and clarifies intent.
