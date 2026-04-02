import re
from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from django.contrib.auth.models import User
from .models import Booking, Room


def homepage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        action = request.POST.get('action', '')

        if action == 'register':
            if not username or not password:
                error_message = 'Username and password are required for registration.'
            elif User.objects.filter(username=username).exists():
                error_message = 'Username already exists. Please choose a different one.'
            else:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('dashboard')
        else: # Default to login behavior if action is login, or not provided
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            error_message = 'Invalid username or password.'

    return render(request, 'home.html', {'error_message': error_message})


@login_required(login_url='home')
def dashboard(request):
    user_bookings = Booking.objects.filter(created_by=request.user)
    now = timezone.localtime()
    today = now.date()
    now_time = now.time()

    # "Upcoming" count shows only Approved bookings
    # "Pending" count includes both Pending and Reschedule statuses
    upcoming_active = user_bookings.filter(status=Booking.Status.APPROVED)
    pending_count = user_bookings.filter(
        status__in=[Booking.Status.PENDING, Booking.Status.RESCHEDULE]
    ).count()

    stats = [
        {
            'label': 'Upcoming',
            'value': upcoming_active.count(),
            'note': 'Meetings ahead',
        },
        {
            'label': 'Pending',
            'value': pending_count,
            'note': 'Awaiting confirmation',
        },
        {
            'label': 'Rooms Used',
            'value': upcoming_active.values('room').distinct().count(),
            'note': 'Across your bookings',
        },
    ]

    # Next booking shows the earliest Approved booking from today onwards
    next_booking = (
        upcoming_active.filter(meeting_date__gte=today)
        .select_related('room')
        .order_by('meeting_date', 'meeting_time')
        .first()
    )

    context = {
        'stats': stats,
        'next_booking': next_booking,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='home')
def booking(request):
    rooms = Room.objects.filter(is_active=True)
    error_message = None
    suggested_title = None
    prev_title = ''
    prev_date = ''
    prev_time = ''
    prev_room = ''

    if request.method == 'POST':
        room_id = request.POST.get('room')
        title = request.POST.get('meeting_title', '').strip()
        meeting_date = request.POST.get('meeting_date')
        meeting_time = request.POST.get('meeting_time')

        # Capture values for re-population on validation failure
        prev_title = title
        prev_date = meeting_date or ''
        prev_time = meeting_time or ''
        prev_room = room_id or ''

        if title and meeting_date and meeting_time and room_id:
            room = rooms.filter(id=room_id).first()
            if room is not None:
                # Title uniqueness check across this user's bookings
                if Booking.objects.filter(created_by=request.user, title__iexact=title).exists():
                    # Strip trailing digits to find base name, then find next free number
                    base = re.sub(r'\d+$', '', title).strip()
                    counter = 2
                    while Booking.objects.filter(created_by=request.user, title__iexact=f"{base}{counter}").exists():
                        counter += 1
                    suggested_title = f"{base}{counter}"
                    error_message = f'A booking named "{title}" already exists. Please use a unique name.'
                else:
                    Booking.objects.create(
                        title=title,
                        meeting_date=meeting_date,
                        meeting_time=meeting_time,
                        room=room,
                        created_by=request.user,
                    )
                    return redirect('status')

    import datetime as dt
    today = timezone.localdate()
    now_time = timezone.localtime(timezone.now()).time()

    # -- Generate "Available Soon" slot recommendations --
    common_times = [
        dt.time(9, 0), dt.time(10, 0), dt.time(11, 0), dt.time(12, 0),
        dt.time(14, 0), dt.time(15, 0), dt.time(16, 0), dt.time(17, 0),
    ]
    active_rooms = list(Room.objects.filter(is_active=True))
    available_suggestions = []
    for delta in range(0, 6):
        check_date = today + timedelta(days=delta)
        for t in common_times:
            if check_date == today and t <= now_time:
                continue
            for room in active_rooms:
                is_taken = Booking.objects.filter(
                    room=room, meeting_date=check_date, meeting_time=t,
                    status__in=[Booking.Status.APPROVED, Booking.Status.PENDING]
                ).exists()
                if not is_taken:
                    label = 'Today' if delta == 0 else ('Tomorrow' if delta == 1 else check_date.strftime('%b %d'))
                    available_suggestions.append({
                        'room_id': str(room.id),
                        'room_name': room.name,
                        'date': check_date.strftime('%Y-%m-%d'),
                        'date_label': label,
                        'time_24': t.strftime('%H:%M'),
                        'time_display': t.strftime('%I:%M %p').lstrip('0'),
                    })
                if len(available_suggestions) >= 6:
                    break
            if len(available_suggestions) >= 6:
                break
        if len(available_suggestions) >= 6:
            break

    # -- Recent approved bookings as re-book templates --
    recent_bookings = (
        Booking.objects.filter(created_by=request.user)
        .select_related('room')
        .order_by('-created_at')[:3]
    )

    context = {
        'rooms': rooms,
        'available_suggestions': available_suggestions,
        'recent_bookings': recent_bookings,

        'error': error_message,
        'suggested_title': suggested_title,
        'prev_title': prev_title,
        'prev_date': prev_date,
        'prev_time': prev_time,
        'prev_room': prev_room,
    }
    return render(request, 'booking.html', context)


@login_required(login_url='home')
def status(request):
    booking_items = (
        Booking.objects.filter(created_by=request.user)
        .select_related('room')
        .order_by('-meeting_date', '-meeting_time')
    )
    rooms = Room.objects.filter(is_active=True)
    return render(request, 'status.html', {'booking_items': booking_items, 'rooms': rooms})


@login_required(login_url='home')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')

@login_required(login_url='home')
def delete_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id, created_by=request.user)
        booking.delete()
    return redirect('status')


@login_required(login_url='home')
def accept_reschedule(request, booking_id):
    """User confirms the auto-rescheduled time is acceptable → mark as Approved."""
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id, created_by=request.user)
        if booking.status == Booking.Status.RESCHEDULE:
            booking.status = Booking.Status.APPROVED
            booking.save()
    return redirect('status')


@login_required(login_url='home')
def edit_booking(request, booking_id):
    """User rejects the auto-rescheduled time and submits their own preferred slot.
    The save goes through the pre_save signal again, so the queue logic re-runs.
    We temporarily delete the old booking so the new slot check is clean."""
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id, created_by=request.user)
        if booking.status in (Booking.Status.RESCHEDULE, Booking.Status.APPROVED):
            room_id = request.POST.get('room')
            title = request.POST.get('meeting_title', booking.title).strip() or booking.title
            meeting_date = request.POST.get('meeting_date')
            meeting_time = request.POST.get('meeting_time')
            room = Room.objects.filter(id=room_id, is_active=True).first() if room_id else booking.room

            if meeting_date and meeting_time and room:
                # Delete old booking first so its slot isn't treated as a conflict
                booking.delete()
                Booking.objects.create(
                    title=title,
                    meeting_date=meeting_date,
                    meeting_time=meeting_time,
                    room=room,
                    created_by=request.user,
                )
    return redirect('status')