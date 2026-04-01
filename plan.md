# Office Meeting Room Booking System - Project Plan

## Feature Assessment

Based on the review of the current codebase (`meetslot/models.py` and `meetslot/views.py`), here is the status of the requested core features:

### 1. Booking System
✅ **Status**: Present.
**Details**: Users can select a room, date, and time, and create a booking. Handled by the `booking` view and the `Booking` model.

### 2. Booking History & Status
✅ **Status**: Present.
**Details**: Users have a `dashboard` and `status` page to view their past and upcoming bookings, and their statuses.

### 3. Availability Checking
❌ **Status**: Missing.
**Details**: Right now, the `booking` view blindly creates a booking without checking if the room is already booked for that specific date and time.
**How to implement**: 
- Modify the `booking` view in `meetslot/views.py`.
- Before creating a new booking, perform a query to check if a booking already exists for the requested `room`, `meeting_date`, and `meeting_time`.
- If a conflict exists, redirect back to the form with an error message (e.g., "Room is already booked for this specific time").

### 4. Room Management
⚠️ **Status**: Partially Present (Missing Frontend UI).
**Details**: The `Room` model exists in the database, but there are no frontend views or templates for an admin to manage (create, update, delete) rooms. Currently, it would have to be done via the Django default Admin panel.
**How to implement**:
- Create a set of views (`room_list`, `room_create`, `room_update`, `room_delete`) in `meetslot/views.py` or restrict to Django Admin based on user preference.
- Assuming custom UI: create simple forms and templates (`room_list.html`, `room_form.html`) that align with the existing UI and restrict access to staff/admins via `@user_passes_test` decorators.

---

## User Review Required

Please review the assessment above. 
> [!IMPORTANT]
> Do you want a **custom Frontend UI** for Room Management (in the web dashboard), or is simply configuring the default **Django Admin** interface sufficient for your admin needs? 

> [!IMPORTANT]
> For **Availability Checking**, do you want a simple conflict check (exact time match) or overlapping time constraints with duration? The current `Booking` model only has a `meeting_time` but no explicit length. Should we just check exact `meeting_time` matches for the given date/room?

## Proposed Changes

### [MODIFY] `meetslot/views.py`
- Modify `booking(request)` to add a database check: `Booking.objects.filter(room=room, meeting_date=meeting_date, meeting_time=meeting_time, status__in=[Booking.Status.PENDING, Booking.Status.APPROVED]).exists()`.
- Add an `error` context variable if a conflict exists.

### [MODIFY] `templates/booking.html`
- Add an error banner to display availability conflict messages to the user if the `error` context variable is set.

---

## Execution Protocol

**When you are ready to proceed, simply command me to "Execute Protocol" and answer the open questions.** 

When the command is issued, I will:
1. Update `views.py` and `booking.html` to introduce the Availability Checking logic constraint.
2. Setup the Room Management interface based on your answer (Custom Frontend or Django Admin).
3. Test and verify the changes locally on the running server.
