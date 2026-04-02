# MeetSlot

MeetSlot is a Django-based booking dashboard with authentication, themed UI pages, database-backed room management, and a smart auto-rescheduling system.

## ✨ Features

- **Smart Auto-Rescheduling:** Automatically finds the next available time slot for conflicting bookings and transparently slots users in with a "Reschedule" status.
- **Smart Suggestions:** The system scans for upcoming available slots and lets users instantly auto-fill the form with 1 click.
- **Recent Re-books:** Quickly clone previous meeting details from the Booking panel.
- **Fluid UI Animations:** Modern, cross-browser page transitions using the `View Transitions API` for seamless navigation.
- **Custom Pickers:** Enhanced grid-based time picker that ditches clunky native browser wheels.
- **Database & Auth:** Includes full user authentication and integrates with MySQL (or SQLite fallback) for production readiness.

## 🛠️ Project Structure

- `manage.py` - Django entrypoint
- `meetslot/settings.py` - App and security configuration
- `meetslot/models.py` - Room and Booking models (includes signal logic)
- `meetslot/views.py` - Page routing, data context, and auth workflow
- `templates/` - HTML templates (`home.html`, `dashboard.html`, `booking.html`, `status.html`)
- `static/` - CSS styling and design system

## 🚀 Setup & Installation

**1. Create and activate a Virtual Environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate # Mac/Linux
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Configure Environment Variables:**
Copy the template and modify the credentials (e.g., your database connection string):
```bash
cp .env.example .env
```

**4. Run Migrations:**
```bash
python manage.py migrate
```

**5. Create a Superuser (Admin):**
```bash
python manage.py createsuperuser
```

**6. Start Development Server:**
```bash
python manage.py runserver
```

## 🗄️ Database Configuration

By default, the project runs on **SQLite** for rapid local setup.

To use **MySQL**, ensure the `mysqlclient` package is installed and set these values in your `.env` file:

- `DB_ENGINE=django.db.backends.mysql`
- `DB_NAME=<database_name>`
- `DB_USER=<database_user>`
- `DB_PASSWORD=<database_password>`
- `DB_HOST=<database_host>`
- `DB_PORT=<database_port>`

Then execute `python manage.py migrate` to structure your database.

## 🔒 Security Notes

- Do not commit `.env`, `.sqlite3` files, or your `venv/` folder.
- Use `DJANGO_SECRET_KEY` in non-debug deployments.
- Set `DJANGO_DEBUG=False` in production.
- Ensure `ALLOWED_HOSTS` represents your valid deployment hostnames.
