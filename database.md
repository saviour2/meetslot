# Database Implementation Plan

Based on the provided configuration schema and the XAMPP Control Panel image, here is the plan to migrate from SQLite to MySQL and connect the frontend to it:

## 1. Analysis of Configuration
The screenshot provided reveals that **XAMPP MySQL is running on port `3307`** (instead of the standard `3306`).
By default, XAMPP's MySQL superuser is `root` with no password (`''`).

We will map this directly into the environment variables shown in the instructions.

## 2. Plan (To-Do List)

1. **Database Creation**: Since the database `meetslot` doesn't exist out of the box in your XAMPP, I will run a short Python script using the already-installed `pymysql` library to connect to `127.0.0.1:3307` and execute `CREATE DATABASE IF NOT EXISTS meetslot;`.
2. **Environment Update**: Update the `.env` file to redirect Django to XAMPP:
   - `DB_ENGINE=django.db.backends.mysql`
   - `DB_NAME=meetslot`
   - `DB_USER=root`
   - `DB_PASSWORD=`
   - `DB_HOST=127.0.0.1`
   - `DB_PORT=3307`
3. **Database Migration**: Since this is a brand new database, all SQLite data will be left behind. I will run `python manage.py migrate` to generate all required tables and schemas inside your XAMPP MySQL database.
4. **Reseed Test User**: Because the database is fresh, I will recreate the test user `testuser1@example.com` / `Test@12345` so you can test logging in from the frontend.
5. **Verify Runtime**: Confirm the frontend dashboard successfully reads and writes data to the MySQL backend without throwing `OperationalError`.

## Protocol Command
Review the port and plan. When ready to transition the app fully to MySQL, just reply with **"Execute Protocol"**.
