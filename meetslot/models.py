from django.conf import settings
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        RESCHEDULE = "reschedule", "Reschedule"

    title = models.CharField(max_length=180)
    meeting_date = models.DateField()
    meeting_time = models.TimeField()
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="bookings")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-meeting_date", "-meeting_time", "-created_at"]

    def __str__(self):
        return f"{self.title} ({self.meeting_date} {self.meeting_time})"

from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.utils.dateparse import parse_date, parse_time

@receiver(pre_save, sender=Booking)
def auto_reschedule_booking(sender, instance, **kwargs):
    if not instance.pk: # Only apply logic for new bookings
        date_obj = instance.meeting_date
        time_obj = instance.meeting_time

        if isinstance(date_obj, str):
            date_obj = parse_date(date_obj)
        if isinstance(time_obj, str):
            time_obj = parse_time(time_obj)

        if not date_obj or not time_obj:
            return

        current_dt = datetime.combine(date_obj, time_obj)
        original_dt = current_dt

        # Iterate until we find a free slot
        while Booking.objects.filter(
            room=instance.room,
            meeting_date=current_dt.date(),
            meeting_time=current_dt.time()
        ).exists():
            current_dt += timedelta(hours=1)

        instance.meeting_date = current_dt.date()
        instance.meeting_time = current_dt.time()

        if current_dt != original_dt:
            instance.status = Booking.Status.RESCHEDULE
        else:
            instance.status = Booking.Status.APPROVED