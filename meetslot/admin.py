from django.contrib import admin
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('title', 'room', 'meeting_date', 'meeting_time', 'status', 'created_by')
    list_filter = ('status', 'meeting_date', 'room')
    search_fields = ('title', 'created_by__username')
