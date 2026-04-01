# MeetSlot

MeetSlot is a Django-based booking dashboard with authentication, themed UI pages, and database-backed room and meeting management.

## Features

- Login/logout workflow
- Dashboard with dynamic booking stats
- Booking form with room selection from database
- Status page with booking history and state chips
- MySQL-ready database configuration through environment variables

## Project Structure

- `manage.py` - Django entrypoint
- `meetslot/settings.py` - app and security configuration
- `meetslot/models.py` - Room and Booking models
- `meetslot/views.py` - page logic and auth flow
- `templates/` - HTML templates
- `static/` - CSS assets

## Prerequisites

- Python 3.13+
- pip
- MySQL Server (optional, for production-like setup)

## Setup

1. Create and activate virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment template and update values:

```bash
cp .env.example .env
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Create admin user (optional):

```bash
python manage.py createsuperuser
```

6. Start development server:

```bash
python manage.py runserver
```

## Database Configuration

By default, the project runs on SQLite for quick local setup.

To use MySQL, set these values in your environment:

- `DB_ENGINE=django.db.backends.mysql`
- `DB_NAME=<database_name>`
- `DB_USER=<database_user>`
- `DB_PASSWORD=<database_password>`
- `DB_HOST=<database_host>`
- `DB_PORT=<database_port>`

Then run:

```bash
python manage.py migrate
```

## Security Notes

- Do not commit `.env`, database files, or local virtual environment folders.
- Use `DJANGO_SECRET_KEY` from environment in non-debug deployments.
- Set `DJANGO_DEBUG=False` in production.
- Set `ALLOWED_HOSTS` to your deployment hostnames.

## Routes

- `/` -> Login page
- `/dashboard/` -> Dashboard
- `/booking/` -> Booking page
- `/status/` -> Booking status history
- `/logout/` -> Logout endpoint (POST)

## Test User

You can create/update a local test user with:

```bash
python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); u,_=User.objects.get_or_create(username='testuser1', defaults={'email':'testuser1@example.com'}); u.set_password('Test@12345'); u.is_active=True; u.save()"
```
