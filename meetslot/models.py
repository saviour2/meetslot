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