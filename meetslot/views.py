from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import Booking, Room


def homepage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        error_message = 'Invalid username or password.'

    return render(request, 'home.html', {'error_message': error_message})


@login_required(login_url='home')
def dashboard(request):
    user_bookings = Booking.objects.filter(created_by=request.user)
    today = timezone.localdate()

    stats = [
        {
            'label': 'Upcoming',
            'value': user_bookings.filter(meeting_date__gte=today).count(),
            'note': 'Meetings ahead',
        },
        {
            'label': 'Pending',
            'value': user_bookings.filter(status=Booking.Status.PENDING).count(),
            'note': 'Awaiting confirmation',
        },
        {
            'label': 'Rooms Used',
            'value': user_bookings.values('room').distinct().count(),
            'note': 'Across your bookings',
        },
    ]

    next_booking = (
        user_bookings.filter(meeting_date__gte=today)
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

    if request.method == 'POST':
        room_id = request.POST.get('room')
        title = request.POST.get('meeting_title', '').strip()
        meeting_date = request.POST.get('meeting_date')
        meeting_time = request.POST.get('meeting_time')

        if title and meeting_date and meeting_time and room_id:
            room = rooms.filter(id=room_id).first()
            if room is not None:
                Booking.objects.create(
                    title=title,
                    meeting_date=meeting_date,
                    meeting_time=meeting_time,
                    room=room,
                    created_by=request.user,
                )
                return redirect('status')

    week_from_today = timezone.localdate() + timedelta(days=7)
    popular_slots_qs = (
        Booking.objects.filter(meeting_date__lte=week_from_today)
        .values('meeting_time')
        .annotate(total=Count('id'))
        .order_by('-total', 'meeting_time')[:5]
    )
    popular_slots = [item['meeting_time'].strftime('%I:%M %p') for item in popular_slots_qs]

    context = {
        'rooms': rooms,
        'popular_slots': popular_slots,
    }
    return render(request, 'booking.html', context)


@login_required(login_url='home')
def status(request):
    booking_items = (
        Booking.objects.filter(created_by=request.user)
        .select_related('room')
        .order_by('-meeting_date', '-meeting_time')
    )
    return render(request, 'status.html', {'booking_items': booking_items})


@login_required(login_url='home')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')